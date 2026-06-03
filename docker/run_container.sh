
#!/usr/bin/env bash
set -euo pipefail

# Simple helper to build the image and run a container for development
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
IMAGE_NAME="scout_nav2:humble"
DOCKERFILE="$REPO_ROOT/docker/Dockerfile"

echo "Building image $IMAGE_NAME..."
docker build -t "$IMAGE_NAME" -f "$DOCKERFILE" "$REPO_ROOT"

echo "Starting container (bind-mounting repo at /ws)..."
DISPLAY_VALUE="${DISPLAY:-:0}"
XAUTHORITY_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [ -f "$XAUTHORITY_FILE" ]; then
    XAUTH_MOUNT=("-v" "$XAUTHORITY_FILE":"$XAUTHORITY_FILE":ro "-e" "XAUTHORITY=$XAUTHORITY_FILE")
else
    echo "Warning: XAUTHORITY file not found at $XAUTHORITY_FILE. If GUI fails, run 'xhost +local:root' on the host."
fi

docker run --rm -it \
	--network host \
	-e DISPLAY="$DISPLAY_VALUE" \
	-e QT_X11_NO_MITSHM=1 \
	${XAUTH_MOUNT[@]} \
	-v /tmp/.X11-unix:/tmp/.X11-unix:rw \
	-v "$REPO_ROOT":/ws \
	-w /ws \
	"$IMAGE_NAME" bash

