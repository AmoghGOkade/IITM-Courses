import random

def simulate_exponential_backoff(n_nodes=10, L=5, simulation_time=10000):
    MAX_STAGE = 7
    nodes = []

    for _ in range(n_nodes):
        stage = 0
        backoff = random.randint(1, 2**(4 + stage))
        nodes.append({'stage': stage, 'counter': backoff, 'tx': 0, 'success': 0, 'collisions': 0})

    slot = 0
    tx_remaining = 0  # how many slots the current transmission still lasts
    total_collisions = 0
    total_successes = 0

    while slot < simulation_time:
        transmitting_nodes = []

        if tx_remaining > 0:
            tx_remaining -= 1
            slot += 1
            continue

        # Decrement backoff for all eligible nodes
        for node in nodes:
            if node['counter'] > 0:
                node['counter'] -= 1

        # Identify which nodes are transmitting now
        for idx, node in enumerate(nodes):
            if node['counter'] == 0:
                transmitting_nodes.append(idx)

        if len(transmitting_nodes) == 0:
            slot += 1
            continue

        # At least one node is transmitting
        for idx in transmitting_nodes:
            nodes[idx]['tx'] += 1

        if len(transmitting_nodes) == 1:
            # Success
            total_successes += 1
            nodes[transmitting_nodes[0]]['success'] += 1
            nodes[transmitting_nodes[0]]['stage'] = 0
            nodes[transmitting_nodes[0]]['counter'] = random.randint(1, 2**(4))
        else:
            # Collision
            total_collisions += 1
            for idx in transmitting_nodes:
                nodes[idx]['collisions'] += 1
                nodes[idx]['stage'] = min(nodes[idx]['stage'] + 1, MAX_STAGE)
                new_backoff = random.randint(1, 2**(4 + nodes[idx]['stage']))
                nodes[idx]['counter'] = new_backoff

        # Transmission takes L slots
        tx_remaining = L - 1
        slot += 1

    total_attempts = sum(node['tx'] for node in nodes)
    total_success = sum(node['success'] for node in nodes)
    total_collision = sum(node['collisions'] for node in nodes)

    throughput = total_success * L / simulation_time  # fraction of time slots used successfully

    return {
        'total_attempts': total_attempts,
        'total_successes': total_success,
        'total_collisions': total_collision,
        'collision_rate': total_collision / total_attempts if total_attempts else 0,
        'success_rate': total_success / total_attempts if total_attempts else 0,
        'throughput': throughput,
        'per_node': [{'tx': n['tx'], 'success': n['success'], 'collisions': n['collisions']} for n in nodes]
    }

