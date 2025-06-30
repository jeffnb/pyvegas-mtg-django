
# Evaluating AI Dev Tools on Real Tasks

## Objective

We wanted to evaluate how different AI coding tools handle simple but real developer tasks. Using a basic Django repo, we tried the following:

- Add a `.gitignore`  
- Convert the repo to use `uv`  
- Write unit tests  
- Upgrade Django  

We used GitHub Copilot, Claude, Jules, and Junie. Here’s how each tool actually performed across those tasks—with real links to PRs and an honest breakdown of pros and cons.

## GitHub Copilot

Copilot integrates deeply with GitHub. You can assign issues directly to it, and it will open a pull request and start working in the background. The PR itself becomes a kind of checklist for what it’s doing.

### Add `.gitignore`  
🔗 [PR #5](https://github.com/jeffnb/pyvegas-mtg-django/pull/5)

- It added a `.gitignore` file, but ironically also checked in every `.pyc` file.
- After requesting removal, it fixed the issue—which was nice.
- PR stayed in draft mode, even after changes were reviewed and accepted.

**Pros:**
- Strong PR description
- Testing plan included
- Fits well into standard GitHub review process

**Cons:**
- No checkboxes in the testing plan
- Needed manual prompting to fix `.pyc` file issue
- Never exits draft mode automatically

### Convert to `uv`  
🔗 [PR #10](https://github.com/jeffnb/pyvegas-mtg-django/pull/10)

- Minimal code changes and mostly correct
- Review feedback (like dependency updates) didn't result in any action

**Pros:**
- Super easy to get started
- Detailed PR with usage instructions
- Updates `README`
- Claimed it tested the changes
- You can view Copilot’s reasoning process

**Cons:**
- No pre-PR customization—all feedback must happen after the draft is created
- Took 7.5 minutes
- Didn't react to feedback about dependencies
- Again, left in draft mode

### Add Testing  
🔗 [PR #15](https://github.com/jeffnb/pyvegas-mtg-django/pull/15)

- Functionally fine. Comparable to Claude.
- Nothing surprising.

**Pros:**
- Explicitly tested admin and URLs
- Used the correct index path
- Included test setup

**Cons:**
- Inconsistent in replying to comments and change requests
- At one point it errored out
- Somehow checked in a DB file—even though `.gitignore` should’ve blocked that

### Upgrade Django  

- Couldn’t use `uv` due to firewall limits, so it defaulted to `pip`
- Didn’t catch the `pyproject.toml` allowing a Python version too low for Django 5.2.3

**Pros:**
- Updated URL settings appropriately
- Fast execution
- Attempted compatibility fixes

**Cons:**
- Skipped over the Python version problem entirely
- Wouldn’t have caught the issue unless `uv` was used

### Bonus: Code Review  

Copilot does this well.

- Inline comments
- Labels nitpicks vs. critical issues
- Feels like a human reviewer

## Claude

Claude requires you to run everything locally. You need GitHub SSH and `gh` CLI configured, but once you're set up, it acts like a developer sitting next to you—very interactive.

### Add `.gitignore`  
🔗 [PR #6](https://github.com/jeffnb/pyvegas-mtg-django/pull/6)

**Pros:**
- Everything happens locally—easy to see what’s going on
- Asks for clarification and permission step-by-step
- PR is created in normal (non-draft) mode
- Includes checkbox-style test plan

**Cons:**
- Slower due to back-and-forth interaction
- Doesn’t automatically run tests
- More setup required

### Convert to `uv`  
🔗 [PR #12](https://github.com/jeffnb/pyvegas-mtg-django/pull/12)

**Pros:**
- Fixes its own mistakes when prompted
- PR description is detailed
- Runs `django check` post-change
- Identifies and prunes unnecessary `requirements.txt` entries

**Cons:**
- Didn’t anticipate the production impact of `django-extensions`
- Specified system-dependent Python version
- Takes longer due to interaction

### Add Testing  
🔗 [PR #16](https://github.com/jeffnb/pyvegas-mtg-django/pull/16)

**Pros:**
- Both unit and integration tests
- PR includes good instructions and coverage summary
- Tests cover views, forms, models
- Decent test data generation

**Cons:**
- Includes fluff tests (e.g., simple model creation)
- Some assumptions about routing
- Not very well documented

### Upgrade Django  

**Pros:**
- Upgraded Python version when needed
- Ran tests and checks
- Included test coverage numbers in PR

**Cons:**
- Missed some outdated links in settings
- Several incorrect commands required rerunning

### Bonus: Code Review  
🔗 [PR #19](https://github.com/jeffnb/pyvegas-mtg-django/pull/19)

**Pros:**
- Thorough feedback

**Cons:**
- One large comment block instead of inline comments
- Tone is more critical than collaborative

## Jules

Jules runs entirely in the browser. It boots a VM, asks you to approve a plan, and executes.

### Add `.gitignore`  
🔗 [PR #7](https://github.com/jeffnb/pyvegas-mtg-django/pull/7)

**Pros:**
- Didn’t commit `.pyc` files
- Fast setup and execution

**Cons:**
- Overrode and lost existing config
- Doesn’t always create PRs (sometimes commits directly)

### Convert to `uv`  
🔗 [PR #13](https://github.com/jeffnb/pyvegas-mtg-django/pull/13)

**Pros:**
- Created an `agents.md` file—interesting touch

**Cons:**
- Missed the task entirely
- Couldn’t parse `README.md` due to case sensitivity
- No `pyproject.toml`
- Didn’t create a PR

## Junie

Junie is like Claude, but integrated into the IDE. You can see terminal output and it offers prompts, but is sometimes too subtle in its feedback.

### Add `.gitignore`  
🔗 [PR #8](https://github.com/jeffnb/pyvegas-mtg-django/pull/8)

**Pros:**
- Terminal is visible
- Can resume where it left off
- Checks for latest GitHub CLI version

**Cons:**
- Minimal PR description
- Authentication errors look like success

### Convert to `uv`  
🔗 [PR #11](https://github.com/jeffnb/pyvegas-mtg-django/pull/11)

**Pros:**
- Clear what it was doing
- PR description is thorough

**Cons:**
- Overengineered shell script
- Added a `.uvignore` file (not supported)
- Missed several steps unless re-prompted

### Add Tests  

**Pros:**
- Broke tests into modules
- Debugged live as it went
- Preemptively switched branches

**Cons:**
- Didn’t use `uv`
- Failed to create PR unless told
- Didn’t pull `main` or push branch remotely

### Upgrade Django  
🔗 [PR #17](https://github.com/jeffnb/pyvegas-mtg-django/pull/17)

**Pros:**
- Tried running server to verify changes
- Updated `pyproject.toml`

**Cons:**
- Didn't release terminal after server run
- Used `pip` instead of `uv`
- Manual dependency editing

## Final Thoughts

Each tool had strengths and tradeoffs:

| Task               | Best Tool | Why                                                 |
|--------------------|-----------|------------------------------------------------------|
| Add `.gitignore`   | Claude    | Clean, local, interactive, no weird file check-ins   |
| Convert to `uv`    | Copilot   | Fast, mostly correct, useful documentation           |
| Add Tests          | Claude    | More coverage, better debugging loop                 |
| Upgrade Django     | Claude    | Detected Python version issues and ran `uv` properly |
| Code Review        | Copilot   | Inline, contextual, balanced tone                    |
