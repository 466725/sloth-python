# macOS Development Environment Setup

A complete guide for setting up **Java**, **Python**, and **TypeScript** development on macOS.

---

## Table of Contents

1. [Package Manager (Homebrew)](#1-package-manager-homebrew)
2. [Version Control (Git)](#2-version-control-git)
3. [Programming Languages & Runtimes](#3-programming-languages--runtimes)
   - [3.1 Java (JDK)](#31-java-jdk)
   - [3.2 Python](#32-python)
   - [3.3 Node.js & TypeScript](#33-nodejs--typescript)
4. [Integrated Development Environments](#4-integrated-development-environments)
   - [4.1 Visual Studio Code](#41-visual-studio-code)
   - [4.2 JetBrains IDEs (Optional)](#42-jetbrains-ides-optional)
5. [Environment Smoke Tests](#5-environment-smoke-tests)
6. [Additional Tools](#6-additional-tools)
   - [6.1 JMeter](#61-jmeter)

---

## 1. Package Manager (Homebrew)

Homebrew is the standard package manager for macOS. Install it first, as all subsequent tools depend on it.

### Install

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Configure PATH (Apple Silicon)

On Apple Silicon Macs (M1/M2/M3/M4), Homebrew installs to `/opt/homebrew`. Add it to your shell profile:

```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zshrc
eval "$(/opt/homebrew/bin/brew shellenv)"
```

### Verify

```bash
brew --version
brew doctor
```

---

## 2. Version Control (Git)

### Install

```bash
brew install git
```

### Configure

Set your global Git identity:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Verify

```bash
git --version
git config --list --global
```

---

## 3. Programming Languages & Runtimes

### 3.1 Java (JDK)

#### Install

Install OpenJDK via Homebrew:

```bash
brew install openjdk
```

Symlink OpenJDK so the system Java wrappers can find it:

```bash
sudo ln -sfn $(brew --prefix)/opt/openjdk/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk.jdk
```

#### Configure

Add `JAVA_HOME` and update `PATH` in `~/.zshrc`:

```bash
echo 'export JAVA_HOME=$(/usr/libexec/java_home)' >> ~/.zshrc
echo 'export PATH="$JAVA_HOME/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

#### Verify

```bash
java -version
javac -version
echo $JAVA_HOME
```

---

### 3.2 Python

#### Install

```bash
brew install python
```

#### Configure

Add Homebrew's Python binary directory to your PATH in `~/.zshrc`:

```bash
echo 'export PATH="$(brew --prefix)/opt/python/libexec/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

#### Verify

```bash
python3 --version
pip3 --version
which python3
```

---

### 3.3 Node.js & TypeScript

#### Install

Install Node.js (includes `npm`):

```bash
brew install node
```

Install TypeScript globally:

```bash
npm install -g typescript
```

#### Verify

```bash
node -v
npm -v
tsc -v
```

---

## 4. Integrated Development Environments

### 4.1 Visual Studio Code

#### Install

```bash
brew install --cask visual-studio-code
```

#### Recommended Extensions

Install common language extensions via the terminal:

```bash
# Java Extension Pack
code --install-extension vscjava.vscode-java-pack

# Python Extension
code --install-extension ms-python.python

# ESLint for TypeScript/JavaScript
code --install-extension dbaeumer.vscode-eslint
```

#### Verify

```bash
code --version
```

---

### 4.2 JetBrains IDEs (Optional)

Install dedicated IDEs for Java and Python development:

```bash
# IntelliJ IDEA (Java)
brew install --cask intellij-idea

# PyCharm (Python)
brew install --cask pycharm
```

---

## 5. Environment Smoke Tests

After installation, verify each language environment by compiling and running a simple program.

### 5.1 Java

Create `HelloWorld.java`:

```java
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Java environment is working!");
    }
}
```

Compile and run:

```bash
javac HelloWorld.java
java HelloWorld
```

---

### 5.2 Python

Run an inline script:

```bash
python3 -c 'print("Python environment is working!")'
```

---

### 5.3 TypeScript

Create `test.ts`:

```typescript
const message: string = "TypeScript environment is working!";
console.log(message);
```

Compile and run:

```bash
tsc test.ts
node test.js
```

---

## 6. Additional Tools

### 6.1 JMeter

Install and launch Apache JMeter for performance testing:

```bash
brew install jmeter
```

Open the JMeter GUI:

```bash
open /opt/homebrew/bin/jmeter
```

Verify the installation:

```bash
jmeter --version
```

