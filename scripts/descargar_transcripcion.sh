#!/data/data/com.termux/files/usr/bin/bash
if [ -z "$1" ]; then
    echo "Uso: $0 URL_DEL_VIDEO"
    exit 1
fi
VID=$(echo "$1" | grep -oE '[a-zA-Z0-9_-]{11}')
python3 -c "
from youtube_transcript_api import YouTubeTranscriptApi
try:
    t = YouTubeTranscriptApi().fetch('$VID', ['es'])
except:
    t = YouTubeTranscriptApi().fetch('$VID', ['en'])
with open('/sdcard/Download/Transcript_$VID.txt', 'w') as f:
    [f.write(s.text+'\n') for s in t]
print('✅ Transcripción guardada en /sdcard/Download/Transcript_$VID.txt')
"
