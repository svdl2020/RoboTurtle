# Process book

Here are some decisions I've made during the process of building :robot:RoboTurtle:turtle:

## insurmountable obstacles and how I overcame them

| Issue | Solution |
|---|---|
| Unsure as of yet if SQL database I envisioned actually adds anything | Unsolved. Probably implementing a very small database to keep track of (the amount of) playlists generated or something just to meet the requirements for the final project. |
|Authorization vs Client Credentials API Workflow. A offers a wider scope (user access), CC offers a higher limit on requests. | Using A, yet to run into issues. |
| I know how to extract the username from an ongoing Spotipy API connection, but how to acquire authorization token without username? | Unsolved. Workaround: user has to enter it on site (or change it in config/use it as command line argument?)
| How to properly analyze the user? | API GET requests for their top tracks and top artists. |
| How to find tracks users dont know but might like? | Unsolved. For now: set a low target_popularity when doing API GET request for recommendations. Maybe later: filter saved/liked and/or favorited tracks from the recommendations (or delete them from the finished playlist)? |
| Actually host the app on a website?| Find a free domain? Rent a domain? |
| Which metrics best suit standard :robot:RoboTurtle:turtle: | Unsolved |
| Which metrics should users be able to edit for special :robot:RoboTurtle:turtle: | Unsolved. |

## Metrics I might like to use

| Metric | Type | Parameters | Description |
|---|---|---|---|
| acousticness | float | 0.0 - 1.0 |   A confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence the track is acoustic. |
| danceability | float | 0.0 - 1.0 | Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable. |
| energy | float | 0.0 - 1.0 | Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy. |
| instrumentalness | float | 0.0 - 1.0 | 0.5+= probably instrumental. Predicts whether a track contains no vocals. “Ooh” and “aah” sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly “vocal”. The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0. |
| popularity | int | 0 - 100 | The popularity of the track. The value will be between 0 and 100, with 100 being the most popular. The popularity is calculated by algorithm and is based, in the most part, on the total number of plays the track has had and how recent those plays are. Note: When applying track relinking via the market parameter, it is expected to find relinked tracks with popularities that do not match min_*, max_*and target_* popularities. These relinked tracks are accurate replacements for unplayable tracks with the expected popularity scores. Original, non-relinked tracks are available via the linked_from attribute of the relinked track response. |
| tempo	| float | ?-? | The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration. |
| time_signature | int | ? | 4 voor techno? --- An estimated overall time signature of a track. The time signature (meter) is a notational convention to specify how many beats are in each bar (or measure). |
| valence | float | 0.0 - 1.0 | A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry). |

Also plan to give users the ability to adjust:
1) the number of recommendations per top track/artist or set of those
2) the number of top tracks/artists to use. 

The resulting amount of tracks is a multiplication of those numbers.

## Metrics presentation ideas:
* energy from :turtle: to :battery:
* tempo from :tao: :turtle: to :rabbit:
* acousticness from :robot: to :violin:
* valence from :cloud: to :sun_with_face:
* instrumentalness :microphone: 
* populariry :seedling: to :evergreen_tree:
* Randomize all metrics :slot_machine: 