from main import app
print("--- APP DEBUG ---")
print(f"User Middleware: {app.user_middleware}")
for i, m in enumerate(app.user_middleware):
    print(f"Item {i}: {m} (Type: {type(m)})")
print("-----------------")
