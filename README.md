# Chicken-Catcher

A fun and interactive PyGame where players catch a chicken that moves randomly around the screen! Test your reflexes and accuracy as you try to catch the chicken as many times as possible before time runs out—or before the chicken escapes.

🎮 Features
Dynamic Gameplay: The chicken moves randomly every few seconds to keep you on your toes.

Score Tracking: Earn points for each successful catch. Every 10 catches adds extra time!

Timers:

Game timer (45 seconds, extendable by catching chickens)

Chicken timer (5 seconds to catch before game over)

Vibration Effect: The chicken shakes slightly for a more challenging experience.

High Score Leaderboard: Your highest score is saved between sessions.

Sound Effects: Catch sounds, game over music, and background music enhance the experience.

Click Penalty: Click outside the chicken 3 times and the game ends.

New High Score Celebration: Get a special message when you beat your previous best.

🕹️ Controls
Enter: Start the game

P: Pause the game

R: Restart after game over

Q: Quit the game

Mouse Click: Catch the chicken

📁 Required Files
Make sure these files are in the same directory as catch_the_chicken.py:

Images:
chicken.png (50x50 recommended)

Sounds:
catch_sound.wav

game_over.wav

background_music.wav

Leaderboard:
leaderboard.txt (will be created automatically)

🚀 How to Run
Install Python (3.7 or later)

Install PyGame:

bash
pip install pygame
Place all required files in the same folder

Run the game:

bash
python catch_the_chicken.py
📊 Scoring
Each catch = 1 point

Every 10 catches = +10 seconds to game timer

New high scores are automatically saved

🛠️ Technical Details
Built with PyGame

Object-oriented design with clear functions

Error handling for missing files

Frame rate: 30 FPS

Screen resolution: 800x600

