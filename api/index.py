from flask import Flask, Response
import requests

app = Flask(__name__)

@app.route('/stream/<path:stream_url>')
def proxy_stream(stream_url):
    stream_url = stream_url.replace('%3A', ':').replace('%2F', '/')
    try:
        response = requests.get(stream_url, stream=True)
        response.raise_for_status()
        return Response(
            response.iter_content(chunk_size=8192),
            content_type=response.headers['Content-Type'],
            headers={'Access-Control-Allow-Origin': '*', 'Cache-Control': 'no-cache'}
        )
    except requests.RequestException as e:
        return Response(f"Error: {str(e)}", status=500)
