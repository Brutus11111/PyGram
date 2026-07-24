from telethon import TelegramClient
from dotenv import load_dotenv
import asyncio
import os
import emoji
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout

load_dotenv("config.env")
api_id = int(os.getenv("api_id"))
api_hash = os.getenv("api_hash")

import asyncio
import os
api_id = 000000
api_hash = "xxxxxxxxxxxxxxx"
session_name = "tg_session"
client = TelegramClient(session_name, api_id, api_hash)
current_chat = None
last_seen_id = 0
running = True
in_chat = True

session = PromptSession()

def remove_emojis(text):
    if not text:
        return text
    return emoji.replace_emoji(text, replace="").strip()

def clear():
    os.system("clear")

def chat_title(chat):
    name = (
    return (
        getattr(chat, "title", None)
        or getattr(chat, "first_name", None)
        or getattr(chat, "username", None)
        or str(getattr(chat, "id", "unknown"))
    )
    return remove_emojis(name)

def sender_title(sender):
    if not sender:
        return "unknown"
    name = (
    return (
        getattr(sender, "title", None)
        or " ".join(
            x for x in [getattr(sender, "first_name", None), getattr(sender, "last_name", None)] if x
        )
        or getattr(sender, "username", None)
        or str(getattr(sender, "id", "unknown"))
    )
    return remove_emojis(name)

async def show_recent(chat, limit=15):
    global last_seen_id
    clear()
    print(f"Chat: {chat_title(chat)}")
    print("-" * 80)
    msgs = []
    async for m in client.iter_messages(chat, limit=limit):
        msgs.append(m)
    msgs.reverse()
    for m in msgs:
        sender = await m.get_sender()
        name = "me" if m.out else sender_title(sender)
        t = m.date.strftime("%Y-%m-%d %H:%M")
        txt = remove_emojis(m.text) if m.text else "[no text]"
        txt = m.text if m.text else "[no text]"
        print(f"[{t}] {name}: {txt}")
        if m.id > last_seen_id:
            last_seen_id = m.id
    print("-" * 80)
    print("Type message + Enter | /r refresh | /b back | /q quit")

async def poll_new_messages(chat):
    global last_seen_id, running, in_chat
    while running and in_chat:
        new_msgs = []
        async for m in client.iter_messages(chat, min_id=last_seen_id, limit=20):
            if not m.out:
            if not m.out:  # skip own sent messages; they're already visible
                new_msgs.append(m)
        if new_msgs:
            new_msgs.reverse()
            for m in new_msgs:
                sender = await m.get_sender()
                name = sender_title(sender)
                t = m.date.strftime("%H:%M")
                txt = remove_emojis(m.text) if m.text else "[no text]"
                print(f"[{t}] {name}: {txt}")
                txt = m.text if m.text else "[no text]"
                # move to start of line, clear it, print message, then restore prompt
                print(f"\r\033[K[{t}] {name}: {txt}")
            print("> ", end="", flush=True)
        # still need to track outgoing IDs so we don't re-fetch them
        async for m in client.iter_messages(chat, min_id=last_seen_id, limit=20):
            if m.id > last_seen_id:
                last_seen_id = m.id
        await asyncio.sleep(2)

async def input_loop(chat):
    global running, in_chat
    with patch_stdout():
        while running and in_chat:
            msg = await session.prompt_async("> ")
            cmd = msg.strip()
            if cmd == "/q":
                running = False
                in_chat = False
                break
            elif cmd == "/b":
                in_chat = False
                break
            elif cmd == "/r":
                await show_recent(chat)
            elif cmd:
                await client.send_message(chat, remove_emojis(cmd))
    while running and in_chat:
        msg = await asyncio.to_thread(input, "> ")
        cmd = msg.strip()
        if cmd == "/q":
            running = False
            in_chat = False
            break
        elif cmd == "/b":
            in_chat = False
            break
        elif cmd == "/r":
            await show_recent(chat)
        elif cmd:
            await client.send_message(chat, cmd)

async def main():
    global current_chat, last_seen_id, in_chat, running
    await client.start()

    while running:
        clear()
        dialogs = await client.get_dialogs(limit=30)
        for i, d in enumerate(dialogs, 1):
            print(f"{i}. {remove_emojis(d.name)}")
        print("\n0. Exit")
        choice = input("Choose chat: ").strip()
            print(f"{i}. {d.name}")
        print("\n0. quit")
        choice = input("Choose your chat: ").strip()
        if choice == "0" or choice == "/q":
            break
        try:
            n = int(choice) - 1
            if n < 0 or n >= len(dialogs):
                print("Invalid choice.")
                await asyncio.sleep(1)
                continue
        except ValueError:
            print("Enter a number.")
                print("Illogical choice")
                await asyncio.sleep(1)
                continue
        except ValueError:
            print("Insert a number")
            await asyncio.sleep(1)
            continue

        current_chat = dialogs[n].entity
        last_seen_id = 0
        in_chat = True

        await show_recent(current_chat)
        await asyncio.gather(
            poll_new_messages(current_chat),
            input_loop(current_chat)
        )

with client:
    client.loop.run_until_complete(main())

