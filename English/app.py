import json
import time

def load_scene(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def run_scene(scene, auto_choices=None):
    """Runs a conversation scene. It prints the dialogue and handles cut-ins."""
    # Print scene header with a blank line above
    print()  # blank line for spacing
    print(f"Scene ID: {scene['scene_id']} (Duration: {scene['duration_sec']} sec)")
    print(f"Topic: {', '.join(scene['topic'])} | Setting: {scene['setting']}")
    print("Speakers:", ', '.join([s['id'] for s in scene['speakers']]))
    print("--- Conversation start ---")

    lines = scene['lines']
    cutins_lookup = {cutin['id']: cutin for cutin in scene['cutins']}
    results = []

    for entry in lines:
        # Handle cut-in events
        if 'event' in entry and entry['event'].startswith('CUTIN'):
            cutin_id = entry['event']
            cutin = cutins_lookup[cutin_id]
            print()  # blank line before cut-in
            print(f"*** CUT-IN: {cutin['prompt']} ***")
            for idx, choice in enumerate(cutin['choices'], 1):
                print(f"  {idx}. {choice['text']}")
            start_time = time.time()
            selected = None

            if auto_choices and cutin_id in auto_choices:
                # simulate automatic selection with a short delay
                time.sleep(0.5)
                selected = auto_choices[cutin_id]
                selected_idx = [i for i, ch in enumerate(cutin['choices']) if ch['id'] == selected][0] + 1
                print(f"(Auto) Selected option {selected_idx}")
                reaction_time = time.time() - start_time
            else:
                try:
                    user_input = input(f"Select your choice (1-{len(cutin['choices'])}) within {cutin['timer_sec']} seconds: ").strip()
                    reaction_time = time.time() - start_time
                    selected_idx = int(user_input) - 1
                    if 0 <= selected_idx < len(cutin['choices']):
                        selected = cutin['choices'][selected_idx]['id']
                    else:
                        selected = None
                except Exception:
                    reaction_time = None
                    selected = None

            # Evaluate correctness
            if selected:
                if selected == cutin['best_choice_id']:
                    correctness = 'Best'
                elif selected in cutin.get('acceptable_choice_ids', []):
                    correctness = 'Acceptable'
                else:
                    correctness = 'NG'
            else:
                correctness = 'NoSelection'

            results.append({
                'cutin_id': cutin_id,
                'selected': selected,
                'reaction_time': reaction_time,
                'correctness': correctness
            })
            print()
        else:
            # Print dialogue line
            print(f"[{entry['spk']}] {entry['text']}")

    # End of conversation
    print()  # blank line before end
    print("--- Conversation end ---")
    print()  # blank line after end
    # Summary of results
    print("Session Summary:")
    for res in results:
        rt = res['reaction_time'] if res['reaction_time'] is not None else float('inf')
        print(f"  {res['cutin_id']}: reaction time={rt:.2f}s, result={res['correctness']}")
        cutin = cutins_lookup[res['cutin_id']]
        if res['correctness'] != 'Best':
            best_choice = next(ch for ch in cutin['choices'] if ch['id'] == cutin['best_choice_id'])
            print(f"    -> Best choice: {best_choice['text']}")
            if cutin.get('follow_up'):
                hint = cutin['follow_up'].get('best_next_line_hint', '')
                if hint:
                    print(f"    -> Hint: {hint}")
    print()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Run conversation practice scene.')
    parser.add_argument('scene_file', help='Path to scene JSON file')
    parser.add_argument('--auto', action='store_true', help='Automatically pick the best choices')
    args = parser.parse_args()
    scene = load_scene(args.scene_file)
    if args.auto:
        auto_map = {cutin['id']: cutin['best_choice_id'] for cutin in scene['cutins']}
        run_scene(scene, auto_choices=auto_map)
    else:
        run_scene(scene)
