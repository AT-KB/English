# English Conversation Practice App

This project provides a minimal command‑line tool for practicing multi‑speaker English conversation. It plays scripted conversations with **cut‑in opportunities**, allowing the learner to choose a response from multiple options. Reaction times and correctness are recorded for later review.

## Project Structure

```
english_conversation_app/
├── app.py             # Main command‑line application
├── requirements.txt   # List of Python dependencies
├── README.md          # Documentation and usage instructions
└── scenes/
    ├── scene_0001.json  # Scenario 1: tipping and cultural expectations
    ├── scene_0002.json  # Scenario 2: work‑life balance in remote work
    ├── scene_0003.json  # Scenario 3: food culture differences
    ├── scene_0004.json  # Scenario 4: travel experiences and personal growth
    └── scene_0005.json  # Scenario 5: personal hobbies and passions
```

- **app.py** – Reads a scenario JSON file and runs the conversation in your terminal. It handles dialogue playback, prompts for cut‑in responses, tracks reaction time, and displays a summary.
- **scenes/** – Directory for scenario files. Each JSON file defines the conversation lines, cut‑in events, response choices, and evaluation logic. You can add additional scenarios here following the same schema as `scene_0001.json`.
- **requirements.txt** – Currently empty aside from a note, because this app only uses Python's standard library. Add dependencies here if you extend the app with extra functionality.

## Usage

1. Install Python 3.8 or higher.
2. (Optional) Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies (none required initially):

   ```bash
   pip install -r requirements.txt
   ```

4. Run a scenario:

   ```bash
   # Replace scene_000X.json with the scenario you want to play (1–5)
   python app.py scenes/scene_0001.json
   ```

   During playback, the script will stop at each cut‑in and prompt you to select a response by number. After the conversation ends, it summarizes your reaction times and correctness.

5. For an automated demonstration that chooses the best responses, use:

   ```bash
   python app.py scenes/scene_0001.json --auto
   ```

## Extending the App

- **Add new scenarios:**
  1. Create a JSON file in the `scenes/` directory.
  2. Follow the structure of the provided scenario files (`scene_0001.json` through `scene_0005.json`), which include:
     - A list of `speakers` with IDs and metadata. Each speaker can have fields such as `gender`, `accent`, and an optional `nationality`. You can adjust these to suit your practice needs. The sample scenarios demonstrate using six nationality options—America (US), United Kingdom (UK), Australia (AU), Singapore (SG), India (IN), and Latin America (LATAM)—and two genders (M, F).
     - A `lines` array containing dialogue turns (`spk` and `text` fields) and `event` markers for cut‑ins.
     - A `cutins` array defining each cut‑in event with its prompt, timer duration, multiple response choices, and which choices are considered best or acceptable.
  3. Run your scenario with `python app.py scenes/your_scene.json`.

- **Customize behavior:**
  - Modify `app.py` to change how reaction times are measured, how scoring works, or to integrate audio playback. See the inline comments for guidance.
  - Add dependencies to `requirements.txt` (e.g., for audio playback or advanced user interfaces) and install them with `pip`.

## License

This project is provided as‑is for educational purposes. Feel free to modify and extend it for your own non‑commercial use.
