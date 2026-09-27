import html

import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Jalsa — Live gaming, made local",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded",
)

LANGUAGES = [
    "English",
    "Hindi",
    "Telugu",
    "Tamil",
    "Kannada",
    "Malayalam",
    "Bengali",
    "Marathi",
    "Gujarati",
    "Punjabi",
]
GAMES = [
    "BGMI",
    "Free Fire MAX",
    "Valorant",
    "GTA V",
    "Minecraft",
    "Counter-Strike 2",
    "Call of Duty",
    "EA Sports FC",
    "Just Chatting",
    "IRL",
]
PAGES = [
    "Home",
    "Browse",
    "Esports",
    "Clips",
    "Following",
    "Creator profile",
    "Creator dashboard",
    "Go live",
    "Admin",
    "Sign in",
]

# All content is sample data; no accounts, video, or payments are connected.
SAMPLE_STREAMS = [
    {
        "id": "s1",
        "creator": "AaravPlays",
        "initials": "AP",
        "title": "Rank push to Conqueror 🔥 squad is ready!",
        "game": "BGMI",
        "language": "Hindi",
        "viewers": 12400,
        "emoji": "🎯",
        "color": "#512f99",
        "duration": "02:18:34",
        "verified": True,
    },
    {
        "id": "s2",
        "creator": "MethiGamer",
        "initials": "MG",
        "title": "Grandmaster grind — Telugu lo maatladukundam",
        "game": "Free Fire MAX",
        "language": "Telugu",
        "viewers": 8700,
        "emoji": "⚡",
        "color": "#963d44",
        "duration": "01:42:08",
        "verified": False,
    },
    {
        "id": "s3",
        "creator": "ByteByByte",
        "initials": "BB",
        "title": "Radiant climb | chill ranked games",
        "game": "Valorant",
        "language": "English",
        "viewers": 5300,
        "emoji": "✦",
        "color": "#a74869",
        "duration": "00:56:12",
        "verified": True,
    },
    {
        "id": "s4",
        "creator": "MiraLive",
        "initials": "ML",
        "title": "Exploring Mumbai in story mode 🏙️",
        "game": "GTA V",
        "language": "Hindi",
        "viewers": 4100,
        "emoji": "🏎️",
        "color": "#33706e",
        "duration": "03:04:51",
        "verified": True,
    },
    {
        "id": "s5",
        "creator": "KarthikCreates",
        "initials": "KC",
        "title": "Building a cozy village together",
        "game": "Minecraft",
        "language": "Tamil",
        "viewers": 2800,
        "emoji": "⛏️",
        "color": "#51784b",
        "duration": "01:17:43",
        "verified": False,
    },
    {
        "id": "s6",
        "creator": "CSNamma",
        "initials": "CN",
        "title": "Premier queue with the gang",
        "game": "Counter-Strike 2",
        "language": "Kannada",
        "viewers": 1950,
        "emoji": "🎖️",
        "color": "#8d6235",
        "duration": "00:38:26",
        "verified": False,
    },
    {
        "id": "s7",
        "creator": "NilaStreams",
        "initials": "NS",
        "title": "Late-night co-op and good vibes",
        "game": "Minecraft",
        "language": "Malayalam",
        "viewers": 1420,
        "emoji": "🌙",
        "color": "#46658a",
        "duration": "02:01:15",
        "verified": False,
    },
    {
        "id": "s8",
        "creator": "KolkataClutch",
        "initials": "KC",
        "title": "Clutch or kick? Bengali ranked",
        "game": "Valorant",
        "language": "Bengali",
        "viewers": 980,
        "emoji": "🎮",
        "color": "#735196",
        "duration": "00:49:02",
        "verified": False,
    },
]

SAMPLE_CLIPS = [
    {
        "id": "c1",
        "creator": "AaravPlays",
        "game": "BGMI",
        "title": "1v4 clutch with 1 HP left 😳",
        "views": "84K",
        "emoji": "🎯",
        "color": "#5c3b9f",
    },
    {
        "id": "c2",
        "creator": "MethiGamer",
        "game": "Free Fire MAX",
        "title": "That last-circle timing though",
        "views": "52K",
        "emoji": "⚡",
        "color": "#a5434e",
    },
    {
        "id": "c3",
        "creator": "ByteByByte",
        "game": "Valorant",
        "title": "The cleanest ace of my life",
        "views": "31K",
        "emoji": "✦",
        "color": "#a84b71",
    },
    {
        "id": "c4",
        "creator": "KarthikCreates",
        "game": "Minecraft",
        "title": "I did not expect that creeper",
        "views": "19K",
        "emoji": "⛏️",
        "color": "#4d784d",
    },
]

SAMPLE_CHAT = [
    ("AaravFan", "That rotation was perfect! 🔥"),
    ("pixel_panda", "Hindi stream gang checking in 🙌"),
    ("RiyaGG", "Clutch incoming, I can feel it"),
    ("chai_and_games", "What sensitivity do you use?"),
    ("NeoPlays", "W stream as always 💜"),
]


def initialize_state():
    """Prepare lightweight demo state that lasts for this browser session."""
    defaults = {
        "page": "Home",
        "streams": [dict(stream) for stream in SAMPLE_STREAMS],
        "clips": [dict(clip) for clip in SAMPLE_CLIPS],
        "selected_stream": "s1",
        "selected_creator": "AaravPlays",
        "followed": set(),
        "liked_clips": set(),
        "chat_messages": list(SAMPLE_CHAT),
        "notifications": [],
        "username": "Guest",
        "demo_role": "Viewer",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def go_to(page, **state_values):
    for key, value in state_values.items():
        st.session_state[key] = value
    st.session_state.page = page


def format_viewers(count):
    return f"{count / 1000:.1f}K" if count >= 1000 else str(count)


def show_stream_card(stream, key_prefix):
    """Render a stream preview with working watch and follow actions."""
    title = html.escape(stream["title"])
    creator = html.escape(stream["creator"])
    game = html.escape(stream["game"])
    language = html.escape(stream["language"])
    st.markdown(
        f"""
        <div class="stream-card">
          <div class="stream-thumb" style="background:linear-gradient(140deg,{stream['color']},#171326 92%)">
            <span class="thumb-emoji">{stream['emoji']}</span>
            <span class="live-pill">● LIVE</span>
            <span class="viewer-pill">◉ {format_viewers(stream['viewers'])}</span>
          </div>
          <div class="card-copy">
            <div class="avatar">{stream['initials']}</div>
            <div class="card-text">
              <div class="card-title">{title}</div>
              <div class="muted">{creator}{'  ✓' if stream['verified'] else ''}</div>
              <div class="muted">{game} · {language}</div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    watch_col, follow_col = st.columns([1, 1])
    with watch_col:
        if st.button("Watch stream", key=f"{key_prefix}_watch_{stream['id']}", use_container_width=True):
            go_to("Stream", selected_stream=stream["id"])
            st.rerun()
    with follow_col:
        is_following = stream["creator"] in st.session_state.followed
        label = "Following" if is_following else "＋ Follow"
        if st.button(label, key=f"{key_prefix}_follow_{stream['id']}", use_container_width=True):
            if is_following:
                st.session_state.followed.remove(stream["creator"])
            else:
                st.session_state.followed.add(stream["creator"])
            st.rerun()


def show_stream_grid(streams, key_prefix, columns_count=3):
    if not streams:
        st.info("No streams match these filters. Try another game or language.")
        return
    columns = st.columns(columns_count)
    for index, stream in enumerate(streams):
        with columns[index % columns_count]:
            show_stream_card(stream, key_prefix)


def show_clip_card(clip, key_prefix="clips"):
    liked = clip["id"] in st.session_state.liked_clips
    st.markdown(
        f"""
        <div class="clip-card">
          <div class="clip-thumb" style="background:linear-gradient(160deg,{clip['color']},#171326)">
            <span>{clip['emoji']}</span><small>▶ {clip['views']} views</small>
          </div>
          <strong>{html.escape(clip['title'])}</strong>
          <div class="muted">{html.escape(clip['creator'])} · {html.escape(clip['game'])}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    like_col, share_col = st.columns(2)
    with like_col:
        if st.button(
            "♥ Liked" if liked else "♡ Like",
            key=f"{key_prefix}_like_{clip['id']}",
            use_container_width=True,
        ):
            if liked:
                st.session_state.liked_clips.remove(clip["id"])
            else:
                st.session_state.liked_clips.add(clip["id"])
            st.rerun()
    with share_col:
        if st.button("↗ Share", key=f"{key_prefix}_share_{clip['id']}", use_container_width=True):
            st.toast("Clip link copied (demo)")


def render_home(streams, preferred_language):
    featured = streams[0] if streams else None
    if featured:
        st.markdown(
            f"""
            <div class="hero">
              <div>
                <div class="eyebrow">YOUR NEXT FAVOURITE STREAM</div>
                <h1>Good games.<br/>Great company.</h1>
                <p>Discover live creators and gaming communities from every corner of India.</p>
                <span class="live-pill">● {format_viewers(featured['viewers'])} watching now</span>
              </div>
              <div class="hero-art" style="background:linear-gradient(140deg,{featured['color']},#171326)">
                <span>{featured['emoji']}</span>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button(f"▶  Watch {featured['creator']} live", key="hero_watch"):
            go_to("Stream", selected_stream=featured["id"])
            st.rerun()

    st.subheader("Live now")
    show_stream_grid(streams[:6], "home")

    st.subheader("Popular games in India")
    game_columns = st.columns(5)
    for index, (game, emoji) in enumerate(
        [("BGMI", "🎯"), ("Free Fire MAX", "⚡"), ("Valorant", "✦"), ("GTA V", "🏎️"), ("Minecraft", "⛏️")]
    ):
        with game_columns[index]:
            if st.button(f"{emoji}  {game}", key=f"home_game_{index}", use_container_width=True):
                st.session_state.game_filter = game
                go_to("Browse")
                st.rerun()

    st.subheader(f"{preferred_language} streams")
    regional = [stream for stream in streams if stream["language"] == preferred_language]
    if regional:
        show_stream_grid(regional, "regional", columns_count=min(3, len(regional)))
    else:
        st.caption(f"No live {preferred_language} streams right now. Browse all live channels instead.")

    st.subheader("Fresh clips")
    clip_columns = st.columns(4)
    for column, clip in zip(clip_columns, st.session_state.clips):
        with column:
            show_clip_card(clip, "home")


def render_browse(streams, preferred_language, search_query):
    st.title("Browse live")
    st.caption("Find your next stream by game, language, or what is happening right now.")
    filter_cols = st.columns(3)
    with filter_cols[0]:
        game = st.selectbox("Game or category", ["All games"] + GAMES, key="browse_game")
    with filter_cols[1]:
        language_options = ["All languages"] + LANGUAGES
        default_language = language_options.index(preferred_language) if preferred_language in language_options else 0
        language = st.selectbox("Stream language", language_options, index=default_language, key="browse_language")
    with filter_cols[2]:
        sort_by = st.selectbox(
            "Sort by",
            ["Recommended", "Most viewers", "Recently started"],
            key="browse_sort",
        )
    results = list(streams)
    if game != "All games":
        results = [stream for stream in results if stream["game"] == game]
    if language != "All languages":
        results = [stream for stream in results if stream["language"] == language]
    if search_query:
        query = search_query.casefold()
        results = [
            stream
            for stream in results
            if query in stream["creator"].casefold()
            or query in stream["title"].casefold()
            or query in stream["game"].casefold()
            or query in stream["language"].casefold()
        ]
    if sort_by == "Most viewers":
        results.sort(key=lambda stream: stream["viewers"], reverse=True)
    elif sort_by == "Recently started":
        results.sort(key=lambda stream: stream["duration"])
    st.caption(f"{len(results)} live stream{'s' if len(results) != 1 else ''}")
    show_stream_grid(results, "browse")


def render_stream(streams):
    stream = next(
        (item for item in streams if item["id"] == st.session_state.selected_stream),
        streams[0] if streams else None,
    )
    if not stream:
        st.info("There are no live streams at the moment.")
        return
    if "demo_stream_notice" in st.session_state:
        st.success(st.session_state.pop("demo_stream_notice"))
    details_col, chat_col = st.columns([2.1, 1])
    with details_col:
        st.markdown(
            f"""
            <div class="player" style="background:radial-gradient(ellipse at 50% 42%,{stream['color']},#101018 72%)">
              <span class="player-live">● LIVE</span>
              <div class="player-emoji">{stream['emoji']}</div>
              <div class="player-note">Stream preview · Video playback is a prototype</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(f"### {html.escape(stream['title'])}")
        st.caption(
            f"{stream['game']} · {stream['language']} · "
            f"◉ {format_viewers(stream['viewers'])} watching · {stream['duration']}"
        )
        creator_cols = st.columns([3, 1, 1, 1])
        with creator_cols[0]:
            if st.button(
                f"◉  {stream['creator']}  {'✓' if stream['verified'] else ''}",
                key="stream_creator",
            ):
                go_to("Creator profile", selected_creator=stream["creator"])
                st.rerun()
        with creator_cols[1]:
            is_following = stream["creator"] in st.session_state.followed
            if st.button("Following" if is_following else "＋ Follow", key="stream_follow"):
                if is_following:
                    st.session_state.followed.remove(stream["creator"])
                else:
                    st.session_state.followed.add(stream["creator"])
                st.rerun()
        with creator_cols[2]:
            if st.button("♡ Subscribe", key="stream_subscribe"):
                go_to("Support creator", selected_creator=stream["creator"])
                st.rerun()
        with creator_cols[3]:
            if st.button("↗ Share", key="stream_share"):
                st.toast("Stream link copied (demo)")
        with st.expander("About this stream"):
            st.write(
                f"{stream['creator']} is live with {stream['game']} in {stream['language']}. "
                "Welcome to the community — keep chat kind and have fun."
            )
            st.write("Schedule: Weekdays at 7:00 PM IST · Recent clips and broadcasts coming soon.")
    with chat_col:
        st.markdown("### Live chat")
        st.caption("Be kind. No spam, hate, or personal information.")
        chat_box = st.container(height=390, border=True)
        with chat_box:
            for username, message in st.session_state.chat_messages[-35:]:
                st.markdown(f"**{html.escape(username)}**  {html.escape(message)}")
        with st.form("chat_form", clear_on_submit=True):
            message = st.text_input("Send a message", max_chars=240, label_visibility="collapsed", placeholder="Say something nice…")
            sent = st.form_submit_button("Send", use_container_width=True)
        if sent:
            clean_message = message.strip()
            if clean_message:
                st.session_state.chat_messages.append((st.session_state.username, clean_message))
                st.rerun()
        with st.expander("Chat settings"):
            st.checkbox("Followers-only chat (demo)", key="followers_chat")
            st.checkbox("Slow mode · 10 seconds (demo)", key="slow_chat")
            st.caption("Moderation actions are illustrative and are not connected to a backend.")


def render_creator_profile(streams):
    creator = st.session_state.selected_creator
    creator_streams = [stream for stream in streams if stream["creator"] == creator]
    current = creator_streams[0] if creator_streams else None
    initials = current["initials"] if current else "".join(part[0] for part in creator.split()[:2]).upper()
    safe_initials = html.escape(initials)
    st.markdown(
        f"""
        <div class="profile-banner"></div>
        <div class="profile-head">
          <div class="profile-avatar">{safe_initials}</div>
          <div><h2>{html.escape(creator)} {'✓' if current and current['verified'] else ''}</h2>
          <div class="muted">{'● LIVE NOW' if current else '○ OFFLINE'} · Indian creator</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("Gaming, good people, and a little bit of chaos. Streaming for the community, one match at a time.")
    c1, c2, c3, c4 = st.columns([1, 1, 1, 4])
    is_following = creator in st.session_state.followed
    with c1:
        if st.button("Following" if is_following else "＋ Follow", key="profile_follow"):
            if is_following:
                st.session_state.followed.remove(creator)
            else:
                st.session_state.followed.add(creator)
            st.rerun()
    with c2:
        if st.button("♡ Subscribe", key="profile_subscribe"):
            go_to("Support creator", selected_creator=creator)
            st.rerun()
    with c3:
        if st.button("↗ Share", key="profile_share"):
            st.toast("Creator link copied (demo)")
    st.caption("Instagram · YouTube · Schedule: weekdays at 7:00 PM IST")
    tab_home, tab_live, tab_clips, tab_schedule, tab_about = st.tabs(
        ["Home", "Live", "Clips", "Schedule", "About"]
    )
    with tab_home:
        if current:
            show_stream_grid([current], "profile_home", columns_count=1)
        else:
            st.info("Offline · Next scheduled stream: Weekdays at 7:00 PM IST")
        st.markdown("**Recent clips**")
        clips = [clip for clip in st.session_state.clips if clip["creator"] == creator]
        if clips:
            clip_columns = st.columns(min(3, len(clips)))
            for column, clip in zip(clip_columns, clips):
                with column:
                    show_clip_card(clip, "profile_home")
        else:
            st.caption("No clips yet.")
    with tab_live:
        if current:
            if st.button("▶ Watch live", key="profile_live"):
                go_to("Stream", selected_stream=current["id"])
                st.rerun()
        else:
            st.info("This creator is offline right now.")
    with tab_clips:
        st.caption("Creator highlights")
        creator_clips = [clip for clip in st.session_state.clips if clip["creator"] == creator]
        if creator_clips:
            cols = st.columns(min(3, len(creator_clips)))
            for column, clip in zip(cols, creator_clips):
                with column:
                    show_clip_card(clip, "profile_clips")
        else:
            st.caption("No clips to show yet.")
    with tab_schedule:
        st.info("Upcoming stream · Weekdays at 7:00 PM IST")
    with tab_about:
        st.write("Creator based in India. Streaming in " + (current["language"] if current else "English") + ".")
        st.write("Community guidelines: be respectful, play fair, and look out for one another.")


def render_clips():
    st.title("Clips")
    st.caption("Quick highlights, clutch plays, and funny moments from Indian gaming streams.")
    game_filter = st.selectbox("Filter clips by game", ["All games"] + GAMES, key="clip_game")
    clips = st.session_state.clips
    if game_filter != "All games":
        clips = [clip for clip in clips if clip["game"] == game_filter]
    clip_columns = st.columns(4)
    for index, clip in enumerate(clips):
        with clip_columns[index % 4]:
            show_clip_card(clip, "clips")
    if not clips:
        st.info("No clips in this category yet.")
    st.divider()
    st.subheader("Make a clip")
    st.caption("Clip creation from a live video is a preview-only feature in this prototype.")
    if st.button("✂ Create a demo clip"):
        st.toast("Clip editor preview — live video is not connected")


def render_esports():
    st.title("Esports in India")
    st.caption("Follow local tournaments, teams, and players.")
    st.subheader("Upcoming tournaments")
    tournaments = [
        ("🏆", "Jalsa Open: BGMI Showdown", "BGMI · 16 teams · Starts today, 7:00 PM IST", "₹1,00,000"),
        ("⚔️", "South India Valorant Cup", "Valorant · Qualifiers · 29 September, 6:00 PM IST", "₹75,000"),
        ("🎮", "Campus Clash: Free Fire MAX", "Free Fire MAX · Registration open · 4 October", "₹50,000"),
    ]
    for icon, name, description, prize in tournaments:
        with st.container(border=True):
            left, middle, right = st.columns([1, 5, 2])
            left.markdown(f"## {icon}")
            middle.markdown(f"**{name}**\n\n{description}")
            right.metric("Prize pool", prize)
            if middle.button(f"Follow event · {name}", key=f"event_{name}"):
                st.toast("Tournament followed (demo)")
    st.subheader("Live esports streams")
    show_stream_grid([stream for stream in st.session_state.streams if stream["game"] in ("BGMI", "Valorant")], "esports")
    st.subheader("Teams to watch")
    st.info("Sample teams: Hyderabad Hydra · Chennai Chargers · Mumbai Mavericks")


def render_following(streams):
    st.title("Following")
    if not st.session_state.followed:
        st.info("Creators you follow will show up here.")
        if st.button("Discover live creators"):
            go_to("Browse")
            st.rerun()
        return
    followed_streams = [
        stream for stream in streams if stream["creator"] in st.session_state.followed
    ]
    show_stream_grid(followed_streams, "following")
    offline_creators = st.session_state.followed - {
        stream["creator"] for stream in followed_streams
    }
    if offline_creators:
        st.subheader("Offline")
        st.write(" · ".join(sorted(offline_creators)))


def render_creator_dashboard(streams):
    st.title("Creator studio")
    st.caption("Your creator workspace · Sample analytics for the last 7 days")
    metrics = st.columns(4)
    metrics[0].metric("Current viewers", "2,418", "+12%")
    metrics[1].metric("Peak viewers", "5,302")
    metrics[2].metric("Followers gained", "+284", "7 days")
    metrics[3].metric("Est. earnings", "₹8,450", "demo")

    tab_overview, tab_manager, tab_analytics, tab_moderation, tab_revenue = st.tabs(
        ["Overview", "Stream manager", "Analytics", "Moderation", "Revenue"]
    )
    with tab_overview:
        st.subheader("Your channel this week")
        analytics = pd.DataFrame(
            {"Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], "Watch hours": [18, 25, 21, 34, 29, 42, 37]}
        )
        st.bar_chart(analytics, x="Day", y="Watch hours", y_label="Hours")
        st.write("💜 Keep going — your community watched 206 hours this week.")
    with tab_manager:
        st.subheader("Stream setup")
        with st.form("stream_setup"):
            title = st.text_input("Stream title", placeholder="What are you playing today?")
            category = st.selectbox(
                "Category",
                ["Gaming", "Esports", "IRL", "Music", "Education", "Technology", "Just Chatting"],
            )
            game = st.selectbox("Game", GAMES)
            language = st.selectbox("Stream language", LANGUAGES, index=LANGUAGES.index("Hindi"))
            tags = st.text_input("Tags", placeholder="ranked, squad, chill")
            thumbnail = st.file_uploader("Thumbnail (optional)", type=["png", "jpg", "jpeg"])
            visibility = st.selectbox("Visibility", ["Public", "Unlisted"])
            mature = st.checkbox("This stream is for mature audiences")
            start = st.form_submit_button("🔴 Start demo stream", use_container_width=True)
        if start:
            if not title.strip():
                st.error("Add a stream title before going live.")
            else:
                stream = {
                    "id": f"demo-{len(st.session_state.streams) + 1}",
                    "creator": st.session_state.username if st.session_state.username != "Guest" else "NewCreator",
                    "initials": "NC",
                    "title": title.strip(),
                    "game": game,
                    "category": category,
                    "language": language,
                    "tags": [tag.strip() for tag in tags.split(",") if tag.strip()],
                    "thumbnail_name": thumbnail.name if thumbnail else None,
                    "visibility": visibility,
                    "mature": mature,
                    "viewers": 1,
                    "emoji": "🎮",
                    "color": "#704bb5",
                    "duration": "00:00:01",
                    "verified": False,
                }
                st.session_state.streams.insert(0, stream)
                st.session_state.selected_stream = stream["id"]
                st.session_state.notifications.insert(0, f"Your demo stream is live: {title.strip()}")
                st.session_state.demo_stream_notice = (
                    f"Your {visibility.lower()} demo stream is live! "
                    "Tags and mature-content settings are saved for this preview."
                )
                st.session_state.page = "Stream"
                st.rerun()
        st.markdown("**OBS setup** · Server: `rtmp://demo.jalsa.live/live` · Stream key: `DEMO-KEY-DO-NOT-USE`")
        st.markdown("Recommended: 1080p · 60 FPS · 6,000 Kbps. This demo key cannot broadcast video.")
    with tab_analytics:
        period = st.selectbox("Analytics period", ["Today", "7 days", "30 days", "90 days"], key="analytics_period")
        st.caption(f"Showing sample analytics for {period}.")
        st.metric("Average viewers", "1,860")
        st.metric("Watch time", "206 hours")
        st.metric("Subscriber growth", "+41")
        st.metric("Viewer retention", "38 min avg.")
    with tab_moderation:
        st.subheader("Community moderation")
        st.toggle("Slow mode · 10 seconds", key="studio_slow")
        st.toggle("Followers-only chat", key="studio_followers")
        st.toggle("Subscriber-only chat", key="studio_subscribers")
        st.text_input("Blocked words", placeholder="Add words separated by commas")
        st.caption("Moderator list, timeouts, bans, and reports are demo-only; nothing is sent to a server.")
    with tab_revenue:
        st.subheader("Revenue overview · mock data")
        revenue = pd.DataFrame(
            {
                "Source": ["Subscriptions", "Donations", "Platform fee", "Creator earnings"],
                "Amount (₹)": [4900, 2400, -730, 6570],
            }
        )
        st.bar_chart(revenue, x="Source", y="Amount (₹)")
        st.metric("Pending payout", "₹1,250")
        st.metric("Completed payouts", "₹5,320")
        st.caption("Payouts and payment methods are simulated. No real money is moved.")


def render_support_creator():
    creator = st.session_state.selected_creator
    st.title("Support a creator")
    st.caption(f"Your support helps {creator} make more of what you love.")
    with st.container(border=True):
        amount = st.radio("Choose an amount", ["₹39", "₹99", "₹249", "Custom"], horizontal=True)
        if amount == "Custom":
            custom_amount = st.number_input("Custom amount (₹)", min_value=1, max_value=50000, value=100)
            amount_value = int(custom_amount)
        else:
            amount_value = int(amount.replace("₹", ""))
        tier = st.selectbox("Membership", ["Supporter · ₹39/month", "Insider · ₹99/month", "MVP · ₹249/month"])
        st.caption("Perks are examples: supporter badge, subscriber chat, and monthly community game.")
        payment_method = st.radio("Payment method", ["UPI", "Card", "Net banking"], horizontal=True)
        if payment_method == "UPI":
            st.text_input("UPI ID", placeholder="name@bank (demo only)")
        elif payment_method == "Card":
            st.text_input("Card number", placeholder="Demo only — do not enter real card details")
        else:
            st.selectbox("Bank", ["Choose your bank", "SBI", "HDFC", "ICICI", "Other"])
        if st.button(f"Continue · ₹{amount_value}", type="primary", use_container_width=True):
            st.info(f"Demo payment preview: ₹{amount_value} via {payment_method}. No payment was taken.")
        if st.button("Simulate failed payment", use_container_width=True):
            st.error("Demo payment failed. No payment was attempted or taken.")


def render_sign_in():
    st.title("Welcome to Jalsa")
    st.caption("Join Indian gaming communities, follow creators, and find your people.")
    sign_in_tab, sign_up_tab = st.tabs(["Sign in", "Create account"])
    with sign_in_tab:
        with st.form("sign_in"):
            email = st.text_input("Email")
            st.text_input("Password", type="password")
            submitted = st.form_submit_button("Sign in", use_container_width=True)
        if submitted:
            if not email.strip():
                st.error("Enter an email to continue.")
            else:
                st.session_state.username = email.split("@")[0][:24]
                st.success(f"Signed in to this local demo as {st.session_state.username}.")
        if st.button("Continue with Google (demo)", key="google_signin"):
            st.info("Google sign-in is a visual demo; authentication is not connected.")
        st.button("Forgot password?", key="forgot_password")
    with sign_up_tab:
        with st.form("sign_up"):
            username = st.text_input("Choose a username")
            new_email = st.text_input("Email address")
            st.text_input("Create a password", type="password")
            role = st.selectbox("I am joining as", ["Viewer", "Creator"])
            created = st.form_submit_button("Create account", use_container_width=True)
        if created:
            if not username.strip() or "@" not in new_email:
                st.error("Add a username and a valid email address.")
            else:
                st.session_state.username = username.strip()[:24]
                st.session_state.demo_role = role
                st.success(f"Demo {role.lower()} profile created for {username.strip()}.")
                if role == "Creator":
                    st.info("Your creator studio is ready. Open Go live to set up a demo stream.")
    st.caption("Authentication and account data are not saved to a server.")


def render_admin(streams):
    st.title("Admin console")
    st.caption("Illustrative platform operations · mock data only")
    metrics = st.columns(5)
    metrics[0].metric("Total users", "128.4K")
    metrics[1].metric("Active today", "18,204")
    metrics[2].metric("Live streams", len(streams))
    metrics[3].metric("Creators", "4,820")
    metrics[4].metric("Reports", "12", "-3")
    tab_reports, tab_streams, tab_content = st.tabs(["Reports", "Streams", "Content"])
    with tab_reports:
        reports = pd.DataFrame(
            [
                {"Type": "Chat message", "Target": "sample_user_01", "Reason": "Spam", "Status": "Needs review"},
                {"Type": "Stream", "Target": "sample_channel", "Reason": "Other", "Status": "Needs review"},
                {"Type": "Clip", "Target": "sample_clip", "Reason": "Copyright", "Status": "Under review"},
            ]
        )
        st.dataframe(reports, hide_index=True, use_container_width=True)
        report = st.selectbox("Select report", reports["Target"].tolist())
        action_col, dismiss_col = st.columns(2)
        with action_col:
            if st.button("Review / take action", key="admin_review"):
                st.toast(f"Opened {report} for demo review")
        with dismiss_col:
            if st.button("Dismiss report", key="admin_dismiss"):
                st.toast(f"Dismissed {report} in this demo")
    with tab_streams:
        for stream in streams[:5]:
            col1, col2, col3 = st.columns([4, 2, 1])
            col1.write(f"**{stream['creator']}** · {stream['title']}")
            col2.caption(f"{stream['game']} · {format_viewers(stream['viewers'])} viewers")
            if col3.button("Feature", key=f"feature_{stream['id']}"):
                st.toast(f"Featured {stream['creator']} (demo)")
    with tab_content:
        st.text_input("Add a game/category", placeholder="e.g. Rocket League")
        if st.button("Add category (demo)"):
            st.toast("Category saved for this preview only")
        st.caption("Account suspensions, stream removals, and user reports require a real protected admin backend.")


initialize_state()

st.markdown(
    """
    <style>
    :root { color-scheme: dark; }
    .stApp { background: #101015; }
    [data-testid="stSidebar"] { background: #15151d; border-right: 1px solid #292831; }
    [data-testid="stSidebar"] h1 { color: #f2ecff; letter-spacing: -.04em; }
    h1, h2, h3 { letter-spacing: -.035em; }
    .muted { color: #aaa7b6; font-size: .86rem; margin-top: .22rem; }
    .eyebrow { color: #c4a2ff; font-size: .75rem; font-weight: 700; letter-spacing: .16em; }
    .hero { display:flex; align-items:center; justify-content:space-between; gap:2rem; min-height:245px; padding:2rem 2.3rem; border:1px solid #30253e; border-radius:20px; background:linear-gradient(115deg,#21182e,#17151e 72%); margin-bottom:.7rem; }
    .hero h1 { font-size:2.65rem; line-height:1.03; margin:.6rem 0; }
    .hero p { color:#bbb6c6; max-width:420px; }
    .hero-art { display:flex; align-items:center; justify-content:center; width:34%; min-height:190px; border-radius:16px; }
    .hero-art span { font-size:5rem; filter:drop-shadow(0 8px 20px #0008); }
    .live-pill,.player-live { background:#eb3f61; color:white; border-radius:5px; padding:.22rem .46rem; font-size:.7rem; font-weight:800; letter-spacing:.04em; }
    .stream-card,.clip-card { border:1px solid #302e39; background:#191920; border-radius:13px; overflow:hidden; margin:.45rem 0 .3rem; transition:transform .16s,border-color .16s; }
    .stream-card:hover,.clip-card:hover { transform:translateY(-2px); border-color:#8662bd; }
    .stream-thumb { height:150px; position:relative; display:flex; align-items:center; justify-content:center; overflow:hidden; }
    .thumb-emoji { font-size:4rem; filter:drop-shadow(0 8px 14px #0009); }
    .live-pill { position:absolute; top:10px; left:10px; }
    .viewer-pill { position:absolute; right:9px; bottom:9px; padding:.2rem .42rem; background:#111d; color:#fff; font-size:.75rem; border-radius:5px; }
    .card-copy { display:flex; align-items:flex-start; gap:.7rem; padding:.8rem; min-height:95px; }
    .avatar,.profile-avatar { display:flex; align-items:center; justify-content:center; flex:0 0 auto; width:38px; height:38px; background:#49316a; color:#f5eaff; border-radius:50%; font-size:.72rem; font-weight:800; }
    .card-text { min-width:0; }
    .card-title { font-weight:650; line-height:1.3; min-height:2.5em; }
    .clip-card { padding:0 0 .65rem; }
    .clip-card strong,.clip-card .muted { display:block; margin:.55rem .7rem 0; }
    .clip-thumb { height:220px; display:flex; align-items:center; justify-content:center; position:relative; border-radius:12px 12px 0 0; }
    .clip-thumb span { font-size:4rem; }
    .clip-thumb small { position:absolute; bottom:8px; right:8px; background:#111d; padding:.2rem .35rem; border-radius:4px; }
    .player { height:410px; border-radius:15px; display:flex; align-items:center; justify-content:center; position:relative; overflow:hidden; }
    .player-live { position:absolute; top:14px; left:14px; }
    .player-emoji { font-size:7rem; filter:drop-shadow(0 8px 20px #0009); }
    .player-note { position:absolute; bottom:12px; right:14px; color:#ddd; font-size:.75rem; }
    .profile-banner { height:130px; border-radius:16px; background:linear-gradient(120deg,#54357b,#983f64 55%,#232038); }
    .profile-head { display:flex; align-items:center; gap:1rem; margin:-27px 0 .6rem 1.4rem; }
    .profile-avatar { width:76px; height:76px; border:4px solid #101015; font-size:1rem; }
    .profile-head h2 { margin:.1rem 0; }
    div.stButton > button { border-radius:9px; transition:all .15s; }
    div.stButton > button:hover { border-color:#a987e4; color:#e8d9ff; }
    @media(max-width:760px) { .hero { padding:1.3rem; min-height:unset; } .hero h1 { font-size:2rem; } .hero-art { min-height:120px; } .player { height:250px; } }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("# ✦ Jalsa")
    st.caption("LIVE · PLAY · BELONG")
    st.markdown("---")
    current_page = st.session_state.page
    if current_page in ("Stream", "Support creator"):
        current_page = "Home"
    selected_page = st.radio(
        "Navigate",
        PAGES,
        index=PAGES.index(current_page) if current_page in PAGES else 0,
        label_visibility="collapsed",
    )
    if selected_page != current_page:
        st.session_state.page = selected_page
    st.markdown("---")
    st.caption(f"Signed in as **{st.session_state.username}** · {st.session_state.demo_role}")
    if st.button("Become a creator", use_container_width=True):
        st.session_state.demo_role = "Creator"
        go_to("Go live")
        st.rerun()

top_left, top_middle, top_right = st.columns([5, 2, 1])
with top_left:
    search_query = st.text_input(
        "Search creators, games, or streams",
        placeholder="⌕  Search creators, games, streams…",
        label_visibility="collapsed",
        key="global_search",
    )
with top_middle:
    preferred_language = st.selectbox(
        "Your language",
        LANGUAGES,
        index=LANGUAGES.index("Hindi"),
        label_visibility="collapsed",
        key="preferred_language",
    )
with top_right:
    if st.button(f"🔔 {len(st.session_state.notifications)}", key="notifications_button", use_container_width=True):
        if st.session_state.notifications:
            st.info(" · ".join(st.session_state.notifications[:3]))
        else:
            st.toast("You're all caught up")

if search_query.strip() and st.session_state.page not in ("Browse", "Stream"):
    st.session_state.page = "Browse"

page = st.session_state.page
streams = st.session_state.streams

if page == "Home":
    render_home(streams, preferred_language)
elif page == "Browse":
    render_browse(streams, preferred_language, search_query.strip())
elif page == "Esports":
    render_esports()
elif page == "Clips":
    render_clips()
elif page == "Following":
    render_following(streams)
elif page == "Creator profile":
    render_creator_profile(streams)
elif page == "Creator dashboard":
    render_creator_dashboard(streams)
elif page == "Go live":
    st.title("Go live on Jalsa")
    st.write("New to streaming? Set up your channel in a few quick steps.")
    st.info("Open **Creator studio → Stream manager** to configure and start a mock live stream.")
    st.markdown("**Beginner OBS setup**\n\n1. Install OBS Studio from its official website.\n2. Copy the demo server and key from Stream manager.\n3. Choose 1080p, 60 FPS, and 6,000 Kbps.\n4. Start a demo stream. Video ingest is not connected in this prototype.")
    if st.button("Open creator studio", type="primary"):
        go_to("Creator dashboard")
        st.rerun()
elif page == "Admin":
    render_admin(streams)
elif page == "Sign in":
    render_sign_in()
elif page == "Stream":
    render_stream(streams)
elif page == "Support creator":
    render_support_creator()
else:
    st.title(page)
    st.info("This section is part of the Jalsa prototype.")
