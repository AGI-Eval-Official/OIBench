import re

# extract the code from the generation
# generation is the response from the model
# language is the language of the code
# return the code

def extract_python_code(generation: str):
    generation = generation.replace("[PYTHON3]", "```python").replace("[/PYTHON3]", "```")
    generation = generation.replace("[PYTHON]", "```python").replace("[/PYTHON]", "```")
    generation = generation.replace("```python3", "```python")

    pattern = re.compile(r"```python\n(.*?)```", re.DOTALL)
    matches = pattern.findall(generation)
    if len(matches) >= 1:
        code_block = matches[0]
        return code_block

    sep_index = generation.find("```")
    if sep_index != -1:
        pattern = re.compile(r"```\n(.*?)```", re.DOTALL)
        matches = pattern.findall(generation)
        if len(matches) >= 1:
            code_block = matches[0]
            return code_block
        elif generation[sep_index + len("```"): sep_index + len("```python")] == "python":
            generation = generation[sep_index + len("```python"):]
        else:
            generation = generation[sep_index + len("```"):]
    return generation


def extract_cpp_code(generation: str):
    generation = generation.replace("[CPP]", "```cpp").replace("[/CPP]", "```")
    generation = generation.replace("[C++]", "```cpp").replace("[/C++]", "```")
    generation = generation.replace("[C]", "```c").replace("[/C]", "```")
    generation = generation.replace("```c++", "```cpp")

    pattern = re.compile(r"```cpp\n(.*?)```", re.DOTALL)
    matches = pattern.findall(generation)
    if len(matches) >= 1:
        code_block = matches[0]
        return code_block

    pattern = re.compile(r"```c\n(.*?)```", re.DOTALL)
    matches = pattern.findall(generation)
    if len(matches) >= 1:
        code_block = matches[0]
        return code_block

    sep_index = generation.find("```")
    if sep_index != -1:
        pattern = re.compile(r"```\n(.*?)```", re.DOTALL)
        matches = pattern.findall(generation)
        if len(matches) >= 1:
            code_block = matches[0]
            return code_block
        elif generation[sep_index + len("```"): sep_index + len("```cpp")] == "cpp":
            generation = generation[sep_index + len("```cpp"):]
        elif generation[sep_index + len("```"): sep_index + len("```c")] == "c":
            generation = generation[sep_index + len("```c"):]
        else:
            generation = generation[sep_index + len("```"):]
    return generation


def extract_java_code(generation: str):
    generation = generation.replace("[JAVA]", "```java").replace("[/JAVA]", "```")

    pattern = re.compile(r"```java\n(.*?)```", re.DOTALL)
    matches = pattern.findall(generation)
    if len(matches) >= 1:
        code_block = matches[0]
        return code_block

    sep_index = generation.find("```")
    if sep_index != -1:
        pattern = re.compile(r"```\n(.*?)```", re.DOTALL)
        matches = pattern.findall(generation)
        if len(matches) >= 1:
            code_block = matches[0]
            return code_block
        elif generation[sep_index + len("```"): sep_index + len("```java")] == "java":
            generation = generation[sep_index + len("```java"):]
        else:
            generation = generation[sep_index + len("```"):]
    return generation



def extract_js_code(generation: str):
    generation = generation.replace("[JAVASCRIPT]", "```javascript").replace("[/JAVASCRIPT]", "```").replace("```js", "```javascript")

    pattern = re.compile(r"```javascript\n(.*?)```", re.DOTALL)
    matches = pattern.findall(generation)
    if len(matches) >= 1:
        code_block = matches[0]
        return code_block

    sep_index = generation.find("```")
    if sep_index != -1:
        pattern = re.compile(r"```\n(.*?)```", re.DOTALL)
        matches = pattern.findall(generation)
        if len(matches) >= 1:
            code_block = matches[0]
            return code_block
        elif generation[sep_index + len("```"): sep_index + len("```javascript")] == "javascript":
            generation = generation[sep_index + len("```javascript"):]
        else:
            generation = generation[sep_index + len("```"):]
    return generation


def extract_code(generation: str, language: str):
    language = language.lower()
    if language in ["python", "py"]:
        return extract_python_code(generation)
    elif language in ["cpp", "c++", "c"]:
        return extract_cpp_code(generation)
    elif language in ["java"]:
        return extract_java_code(generation)
    elif language in ["javascript", "js"]:
        return extract_js_code(generation)
    return generation