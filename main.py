import streamlit as st
st.write("🔑 Available secrets:", list(st.secrets.keys()))

#from auth import auth
import datetime
from firebase_config import init_firebase

#USER LOGIN
#if "user" not in st.session_state:
 #   st.session_state.user = None




# Initialize Firebase
db, bucket = init_firebase()


st.set_page_config(page_title="Family Connect", layout="centered")
st.title("👨‍👩‍👧‍👦 Welcome to Family Connect MVP")

st.header("🎂 Add a Birthday / Family Event")

with st.form("event_form"):
    name = st.text_input("Name")
    event_type = st.selectbox("Event Type", ["Birthday", "Anniversary", "Reunion"])
    date = st.date_input(
        "Event Date",
        value=datetime.date.today(),
        min_value=datetime.date(1920, 1, 1),
        max_value=datetime.date(2100, 12, 31)
    )
    submitted = st.form_submit_button("Add Event")

    if submitted:
        db.collection("events").add({
            "name": name,
            "type": event_type,
            "date": date.strftime("%Y-%m-%d")
        })
        st.success(f"{event_type} for {name} on {date} added!")

st.subheader("📆 Family Events")

events = db.collection("events").order_by("date").stream()

st.header("🗞️ Family News Feed")

with st.form("news_form"):
    author = st.text_input("Your Name")
    post = st.text_area("What's new in the family?")
    submitted = st.form_submit_button("Post")

    if submitted:
        db.collection("posts").add({
            "author": author,
            "content": post,
            "timestamp": datetime.datetime.now().isoformat()
        })
        st.success("Your update has been posted!")

st.header("📸 Upload a Family Photo")

uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    from uuid import uuid4
    import tempfile

    file_id = str(uuid4())
    file_name = f"photos/{file_id}_{uploaded_file.name}"
    blob = bucket.blob(file_name)

    # Save file temporarily and upload
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_file_path = tmp_file.name
        blob.upload_from_filename(tmp_file_path)

    blob.make_public()  # Make the image accessible by URL
    image_url = blob.public_url

    db.collection("photos").add({
        "url": image_url,
        "uploaded_at": datetime.datetime.now().isoformat()
    })

    st.success("✅ Photo uploaded!")
    st.image(image_url, caption="Preview", width=300)

st.subheader("🖼️ Family Photo Album")

photos = db.collection("photos").order_by("uploaded_at", direction="DESCENDING").stream()

for p in photos:
    data = p.to_dict()
    st.image(data["url"], width=300)
    st.caption(f"📅 Uploaded at {data['uploaded_at']}")

st.header("📇 Add Family Member to Directory")

with st.form("directory_form"):
    full_name = st.text_input("Full Name")
    relation = st.selectbox("Relation", [
        "Parent", "Sibling", "Cousin", "Grandparent", "Uncle/Aunt", "Child", "Other"
    ])
    email = st.text_input("Email (optional)")
    phone = st.text_input("Phone (optional)")

    submitted = st.form_submit_button("Add to Directory")

    if submitted and full_name and relation:
        db.collection("directory").add({
            "name": full_name,
            "relation": relation,
            "email": email,
            "phone": phone,
            "added_at": datetime.datetime.now().isoformat()
        })
        st.success(f"{full_name} added to the directory!")

st.subheader("👨‍👩‍👧‍👦 Family Directory")

members = db.collection("directory").order_by("name").stream()

for m in members:
    data = m.to_dict()
    st.markdown(f"**{data['name']}** – {data['relation']}")
    if data.get("email"):
        st.write(f"📧 {data['email']}")
    if data.get("phone"):
        st.write(f"📱 {data['phone']}")
    st.markdown("---")


st.subheader("📬 Latest Posts")

posts = db.collection("posts").order_by("timestamp", direction="DESCENDING").stream()

for post in posts:
    data = post.to_dict()
    st.markdown(f"**{data['author']}** wrote:")
    st.write(f"> {data['content']}")
    st.caption(f"🕒 {data['timestamp']}")


for e in events:
    data = e.to_dict()
    st.write(f"**{data['type']}** – {data['name']} on {data['date']}")

