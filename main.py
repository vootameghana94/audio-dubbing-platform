import os
import subprocess
from gtts import gTTS
from pydub import AudioSegment

# ============================================
# SETTINGS
# ============================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_VIDEO = os.path.join(BASE_DIR, "input", "The Lion and the Mouse.mp4")

# Languages to generate
JOBS = [
    {
        "name": "Telugu",
        "code": "te",
        "file": "Pure_Telugu_Translation.mp4",
        "text": """సింహం మరియు ఎలుక కథ. ఒక చిన్న ఎలుక నిద్రపోతున్న సింహం మీద ఆడుకుంటూ పరిగెడుతోంది. సింహం నిద్రలేచి ఎలుకను తన పంజాతో పట్టుకుంది. దయచేసి నన్ను తినవద్దు, నేను ఒకరోజు నీకు సహాయం చేస్తాను అని ఎలుక వేడుకుంది. సింహం నవ్వింది, కానీ దయతో ఎలుకను వదిలేసింది. కొన్ని రోజుల తర్వాత, సింహం వలలో చిక్కుకుంది. ఎలుక వచ్చి వల తాడులను కొరికివేసింది. సింహం విముక్తి పొందింది!"""
    },
    {
        "name": "Hindi",
        "code": "hi",
        "file": "Pure_Hindi_Translation.mp4",
        "text": """शेर और चूहा। एक छोटा चूहा सोए हुए शेर के ऊपर खेल रहा था। शेर जाग गया और उसने चूहे को अपने पंजे में पकड़ लिया। चूहा बोला, कृपया मुझे मत खाओ, मैं एक दिन तुम्हारी मदद करूँगा। शेर हँसा, लेकिन उसने चूहे को जाने दिया। कुछ दिनों बाद, शेर एक शिकारी के जाल में फंस गया। चूहे ने अपने तेज़ दाँतों से रस्सियों को काट दिया। शेर आज़ाद हो गया!"""
    }
]

os.makedirs(os.path.join(BASE_DIR, "output"), exist_ok=True)

# ============================================
# PROCESSING
# ============================================
for job in JOBS:
    print(f"\n🎙️ Processing {job['name']}...")

    # 1. Generate Voice Audio
    temp_voice = os.path.join(BASE_DIR, "output", f"temp_{job['code']}.mp3")
    tts = gTTS(text=job['text'], lang=job['code'])
    tts.save(temp_voice)

    # 2. FFmpeg Mix (Video + Translation ONLY)
    output_path = os.path.join(BASE_DIR, "output", job['file'])

    # EXPLANATION:
    # -map 0:v:0  -> Take the video/pictures from the original file
    # -map 1:a:0  -> Take the audio ONLY from our new translation
    # This completely ignores/deletes the original English sound.
    cmd = [
        'ffmpeg',
        '-i', INPUT_VIDEO,
        '-i', temp_voice,
        '-c:v', 'copy',
        '-map', '0:v:0',
        '-map', '1:a:0',
        '-shortest',
        output_path,
        '-y'
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"✅ SUCCESS: Saved to output/{job['file']}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e.stderr.decode()}")

print("\n✨ Done! You now have two video files with NO English and NO background music.")