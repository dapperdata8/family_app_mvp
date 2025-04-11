import streamlit as st
from firebase_config import init_firebase
import datetime

# Initialize Firebase
db, bucket = init_firebase()

st.title("👨‍👩‍👧‍👦 Family App MVP")

# Birthday Entry
st.header("🎂 Add a Family Birthday")
name = st.text_input("Name")
birthdate = st.date_input("Birthdate", min_value=datetime.date(1920, 1, 1))
if st.button("Add Birthday"):
    doc_ref = db.collection("birthdays").document()
    doc_ref.set({"name": name, "birthdate": str(birthdate)})
    st.success(f"Added birthday for {name}")

# Show Birthdays
st.header("📅 Upcoming Birthdays")
birthdays = db.collection("birthdays").stream()
for b in birthdays:
    b_data = b.to_dict()
    st.write(f"{b_data['name']} - {b_data['birthdate']}")

# Post Family Update
st.header("📰 Post Family Update")
update_text = st.text_area("Write an update")
if st.button("Post Update"):
    db.collection("updates").add({"text": update_text, "timestamp": datetime.datetime.now()})
    st.success("Update posted!")

# Show Updates
st.header("🧾 Latest Updates")
updates = db.collection("updates").order_by("timestamp", direction="DESCENDING").limit(5).stream()
for update in updates:
    u_data = update.to_dict()
    st.markdown(f"**{u_data['timestamp']}**: {u_data['text']}")