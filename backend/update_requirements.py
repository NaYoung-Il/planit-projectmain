import subprocess
import os

# 1. 직접 설치한 패키지 목록 가져오기
try:
    print("Running: pip list --not-required --format=freeze")
    not_required = subprocess.check_output(
        ["pip", "list", "--not-required", "--format=freeze"],
        text=True
    ).splitlines()
except subprocess.CalledProcessError as e:
    print("Error: pip list failed:", e)
    not_required = []

# 2. 전체 패키지 목록 가져오기 (pip freeze)
try:
    installed = subprocess.check_output(["pip", "freeze"], text=True).splitlines()
except subprocess.CalledProcessError as e:
    print("Error: pip freeze failed:", e)
    installed = []

# 3. 기존 requirements.txt 읽기
if os.path.exists("requirements.txt"):
    with open("requirements.txt", "r") as f:
        existing = set(f.read().splitlines())
else:
    existing = set()

# 4. 새로 추가된 패키지 필터링
new_packages = [pkg for pkg in installed if pkg not in existing]

# 5. requirements.txt 업데이트
if new_packages:
    with open("requirements.txt", "a") as f:
        f.write("\n".join(new_packages) + "\n")
    print(f"{len(new_packages)} new packages added:")
    for p in new_packages:
        print(" +", p)
else:
    print("No new packages found.")

