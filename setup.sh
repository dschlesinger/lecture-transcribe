sudo apt update

sudo apt install ffmpeg

python -m venv .venv

sudo chmod +x .venv/bin/activate

.venv/bin/activate

pip install --upgrade google-api-python-client \
                        google-auth-httplib2 \
                        google-auth-oauthlib \
                        openai-whisper \
                        setuptools-rust \
                        python-dotenv \

# Check Python Version compatability
python utils/version_tools.py
