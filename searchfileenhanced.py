import os
import time
from collections import deque
import google.generativeai as genai

# ------------------------------
# 🔑 Gemini API Setup
# ------------------------------
GEMINI_API_KEY = ""   # 🔴 PUT YOUR API KEY HERE
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


# ------------------------------
# Gemini Processing
# ------------------------------
def use_gemini(file_path):
    print("\n🤖 Gemini Processing...")

    try:
        with open(file_path, 'r') as f:
            content = f.read()

        response = model.generate_content(
            f"Analyze this file content:\n{content}"
        )

        print("\n🧠 Gemini Response:\n")
        print(response.text[:500])

    except Exception as e:
        print("⚠️ Gemini Error:", e)


# ------------------------------
# DFS (Stack)
# ------------------------------
def search_dfs(base_path, target):
    start = time.time()
    stack = [base_path]

    while stack:
        current = stack.pop()

        try:
            for item in os.listdir(current):
                full = os.path.join(current, item)

                if os.path.isfile(full) and item == target:
                    return full, time.time() - start

                elif os.path.isdir(full):
                    stack.append(full)
        except PermissionError:
            continue

    return None, time.time() - start


# ------------------------------
# BFS (Queue)
# ------------------------------
def search_bfs(base_path, target):
    start = time.time()
    queue = deque([base_path])

    while queue:
        current = queue.popleft()

        try:
            for item in os.listdir(current):
                full = os.path.join(current, item)

                if os.path.isfile(full) and item == target:
                    return full, time.time() - start

                elif os.path.isdir(full):
                    queue.append(full)
        except PermissionError:
            continue

    return None, time.time() - start


# ------------------------------
# os.walk
# ------------------------------
def search_walk(base_path, target):
    start = time.time()

    for root, dirs, files in os.walk(base_path):
        if target in files:
            return os.path.join(root, target), time.time() - start

    return None, time.time() - start


# ------------------------------
# Linear Search
# ------------------------------
def search_linear(base_path, target):
    start = time.time()
    file_list = []

    for root, dirs, files in os.walk(base_path):
        for f in files:
            file_list.append(os.path.join(root, f))

    for file in file_list:
        if os.path.basename(file) == target:
            return file, time.time() - start

    return None, time.time() - start


# ------------------------------
# Binary Search
# ------------------------------
def search_binary(base_path, target):
    start = time.time()
    file_list = []

    for root, dirs, files in os.walk(base_path):
        for f in files:
            file_list.append(os.path.join(root, f))

    # Sort by filename
    file_list.sort(key=lambda x: os.path.basename(x))

    left, right = 0, len(file_list) - 1

    while left <= right:
        mid = (left + right) // 2
        name = os.path.basename(file_list[mid])

        if name == target:
            return file_list[mid], time.time() - start
        elif name < target:
            left = mid + 1
        else:
            right = mid - 1

    return None, time.time() - start


# ------------------------------
# Create File
# ------------------------------
def create_file(base_path, file_name):
    path = os.path.join(base_path, file_name)
    with open(path, 'w') as f:
        f.write("This file was created automatically.\n")
    return path


# ------------------------------
# SMART ALGORITHM SELECTION
# ------------------------------
def choose_algorithm(base_path):
    folder_count = 0
    max_depth = 0

    for root, dirs, files in os.walk(base_path):
        folder_count += len(dirs)
        depth = root.count(os.sep)
        max_depth = max(max_depth, depth)

    if folder_count < 5:
        return "LINEAR", "Small number of folders → Linear search is efficient"

    elif max_depth > 3:
        return "DFS", "Directory is deep → DFS is faster for deep traversal"

    elif folder_count > 10:
        return "BFS", "Many folders at same level → BFS is better for wide structure"

    else:
        return "WALK", "General case → os.walk is optimized for traversal"


# ------------------------------
# MAIN FUNCTION
# ------------------------------
def run_smart():
    print("===== SMART AI FILE SEARCH SYSTEM =====")

    base_path = os.getcwd()
    file_name = input("Enter file name: ").strip()

    algo, reason = choose_algorithm(base_path)

    print(f"\n🤖 Selected Algorithm: {algo}")
    print(f"📌 Reason: {reason}")

    # Run selected algorithm
    if algo == "DFS":
        path, t = search_dfs(base_path, file_name)

    elif algo == "BFS":
        path, t = search_bfs(base_path, file_name)

    elif algo == "LINEAR":
        path, t = search_linear(base_path, file_name)

    elif algo == "BINARY":
        path, t = search_binary(base_path, file_name)

    else:
        path, t = search_walk(base_path, file_name)

    # ------------------------------
    # RESULT
    # ------------------------------
    if path:
        print("\n✅ File FOUND at:", path)
    else:
        print("\n❌ File NOT FOUND → Creating...")
        path = create_file(base_path, file_name)
        print("✅ File CREATED at:", path)

    print(f"\n⏱ Time Taken: {t:.6f} seconds")

    # ------------------------------
    # COMPLEXITY
    # ------------------------------
    complexity = {
        "DFS": ("O(N)", "O(H)"),
        "BFS": ("O(N)", "O(W)"),
        "WALK": ("O(N)", "O(H)"),
        "LINEAR": ("O(N)", "O(N)"),
        "BINARY": ("O(N log N)", "O(N)")
    }

    t_comp, s_comp = complexity.get(algo, ("O(N)", "O(H)"))

    print("\n📊 COMPLEXITY:")
    print(f"{algo} → Time: {t_comp}, Space: {s_comp}")

    # ------------------------------
    # GEMINI
    # ------------------------------
    use_gemini(path)

    # ------------------------------
    # FINAL CONCLUSION
    # ------------------------------
    print("\n📌 FINAL CONCLUSION:")
    print(f"{algo} was selected because: {reason}")
    print(f"It completed the search in {t:.6f} seconds.")


# ------------------------------
# RUN
# ------------------------------
if __name__ == "__main__":
    run_smart()
