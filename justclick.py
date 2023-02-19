import os
import json
import time
print("Traversing all the folders and files.....")
time.sleep(1)
print("Generating data.....")
time.sleep(1)
print("Creating brand new website.....!")
time.sleep(1)
def get_directory_structure(rootdir):
    """
    Create a nested JSON object that represents the folder structure of rootdir
    """
    dir = {}
    rootdir = rootdir.rstrip(os.sep)
    start = rootdir.rfind(os.sep) + 1
    for path, dirs, files in os.walk(rootdir):
        folders = path[start:].split(os.sep)
        subdir = {}
        numerical_files = []
        other_files = []
        for file in files:
            try:
                numerical_prefix = int(file.split('.')[0])
                numerical_files.append((numerical_prefix, file))
            except ValueError:
                other_files.append(file)
        sorted_numerical_files = sorted(numerical_files, key=lambda x: x[0])
        sorted_other_files = sorted(other_files)
        sorted_files = [f[1] for f in sorted_numerical_files] + sorted_other_files
        for file in sorted_files:
            subdir[file] = None
        parent = dir
        for folder in folders[1:]:
            if folder not in parent:
                parent[folder] = {}
            parent = parent[folder]
        parent.update(subdir)

        numerical_dirs = []
        other_dirs = []
        for folder in dirs:
            try:
                numerical_prefix = int(folder.split('.')[0])
                numerical_dirs.append((numerical_prefix, folder))
            except ValueError:
                other_dirs.append(folder)
        sorted_numerical_dirs = sorted(numerical_dirs, key=lambda x: x[0])
        sorted_other_dirs = sorted(other_dirs)
        sorted_dirs = [f[1] for f in sorted_numerical_dirs] + sorted_other_dirs
        dirs[:] = sorted_dirs
    return dir


# Use the function
root_directory = '.'
directory_structure = get_directory_structure(root_directory)
data = json.dumps(directory_structure, indent=2)





courseInfo = '''
directoryStructure = {coursedata}
'''
courseInfo = courseInfo.format(coursedata=data)

js = '''


//!expanding HTML
Object.keys(directoryStructure).forEach((a) => {
  if (
    a.endsWith(".ini") ||
    a.endsWith(".py") ||
    a.endsWith(".zip") ||
    a.endsWith(".png")
  ) {
    console.log("pass");
  } else {
    document.title = a;
  }
});

function lastPlayed() {

  const lastViewed = localStorage.getItem(document.title);

  if (!lastViewed) {
    return;
  }
  const milestone_image = document.querySelector(".milestoneImage");
  const title = document.querySelector(".title");
  const video = document.querySelector(".video");
  milestone_image.style.display = "none";
  video.src = lastViewed;
  video.style.display = "block";
  const nameArr = lastViewed.split("/");
  title.innerText = nameArr[nameArr.length - 1].replace(/\.[^/.]+$/, "");
  video.style.opacity = "1";
}

function createFolders(structure, path = "") {
  return Object.entries(structure).map(([key, value]) => {
    let fullPath = path ? path + "/" + key : key;
    if (value === null) {
      return key.endsWith(".py") ||
        key.endsWith(".srt") ||
        key.endsWith(".ini") ||
        key.endsWith(".exe")
        ? ""
        : `<p onclick="playModule(this)" id="${fullPath}" class="files"><i class="fa-regular ${
            key.endsWith(".txt")
              ? "fa-file-lines"
              : key.endsWith(".pdf")
              ? "fa-file-pdf"
              : key.endsWith(".png")
              ? "fa-image"
              : key.endsWith(".jpg")
              ? "fa-image"
              : key.endsWith(".docx")
              ? "fa-file-word"
              : key.endsWith(".mp4") ||
                key.endsWith(".m4v") ||
                key.endsWith(".avi")
              ? "fa-circle-play"
              : key.endsWith(".zip")
              ? "fa-file-zipper"
              : "fa-file-code"
          }"></i> ${
            key.endsWith(".mp4") || key.endsWith("m4v") || key.endsWith("avi")
              ? key.replace(/\.[^/.]+$/, "")
              : key
          }</p>`;
    }
    let folderContent = createFolders(value, fullPath).join("");
    let folder = !key.startsWith(".")
      ? `<div class="folder">
        <p><i class="fa fa-folder"></i> ${key} <i class="fa-solid fa-caret-right"></i></p>
        <div class="nested-folder">${folderContent}</div>
      </div>`
      : "";
    return folder;
  });
}

document.addEventListener("DOMContentLoaded", function () {
  lastPlayed();
  const milestones = document.querySelector(".milestones");
  milestones.innerHTML = createFolders(directoryStructure).join("");
  let clicked = "this is the text of milestone";

  let folders = document.getElementsByClassName("folder");
  for (let folder of folders) {
    folder.addEventListener("click", function (event) {
      let target = event.target;

      const caret = target.querySelectorAll("i")[1];

      if (caret.classList.contains("fa-caret-down")) {
        caret.classList.replace("fa-caret-down", "fa-caret-right");
      } else {
        caret.classList.replace("fa-caret-right", "fa-caret-down");
      }
      if (clicked != target.innerText && !target.classList.contains("files")) {
        target.click();
        caret.classList.replace("fa-caret-right", "fa-caret-down");
      }
      clicked = target.innerText;

      if (target.classList.contains("files")) {
        return;
      }
      let nestedFolder = folder.getElementsByClassName("nested-folder")[0];
      if (nestedFolder.style.display === "none") {
        nestedFolder.style.display = "block";
      } else {
        nestedFolder.style.display = "none";
      }
      event.stopPropagation();
    });
  }
});

function playModule(elem) {
  const title = document.querySelector(".title");
  const video = document.querySelector(".video");
  const milestone_image = document.querySelector(".milestoneImage");
  const active = document.querySelector(".activeColor");
  video.style.opacity = "0";
  video.volume = 0.9;

  if (active && !elem.classList.contains("activeColor")) {
    active.classList.remove("activeColor");
  }

  // toggle current clicked one
  elem.classList.toggle("activeColor");
  const module_name = elem.innerText;
  const source = `./${elem.getAttribute("id")}`;
  const ext = source.split(".").at(-1);
  console.log(source.split(".").at(-1));
  let ifnotMedia =
    ext === "txt" ||
    ext === "pdf" ||
    ext === "docx" ||
    ext === "png" ||
    ext === "jpeg" ||
    ext === "jpg" ||
    ext === "html" ||
    ext === "cpp" ||
    ext === "c" ||
    ext === "ppt" ||
    ext === "pptx" ||
    ext === "zip";
  // elem.innerText.endsWith(".pdf") ||
  //   elem.innerText.endsWith(".png") ||
  //   elem.innerText.endsWith(".docx") ||
  //   elem.innerText.endsWith(".zip") ||
  //   elem.innerText.endsWith(".html") ||
  //   elem.innerText.endsWith(".jpg");
  if (ifnotMedia) {
    return showPdf(source);
  }
  milestone_image.style.display = "none";
  // const Homework = source.includes("Homework");
  // const Solution = source.includes("Homework");
  // if (Homework && !Solution) {
  //   window.alert("Please Complete the Homework");
  // }
  video.src = source;
  video.style.display = "block";
  title.innerText = module_name;
  video.style.opacity = "1";
  localStorage.setItem(document.title, source);
}

// more functionality: user can only expand next milestone if they completed previous course

function doc_keyUp(e) {
  e.preventDefault();
  const video = document.querySelector(".video");
  //video SpeedUp;
  if (e.shiftKey && e.keyCode === 190) {
    video.playbackRate += 0.1;
  }
  //video SpeedDown;
  if (e.shiftKey && e.keyCode === 188) {
    video.playbackRate -= 0.1;
  }
  //volume up
  if (e.key === "ArrowUp") {
    video.volume += 0.1;
  }
  //volume down
  if (e.key === "ArrowDown") {
    video.volume -= 0.1;
  }
  //pause video
  if (e.key == " " || e.code == "Space" || e.keyCode == 32) {
    document.querySelector("[data-plyr=play]").click();
  }

  if (e.key === "ArrowRight") {
    video.currentTime += 10;
  }
  if (e.key === "ArrowLeft") {
    video.currentTime -= 10;
  }
  if (e.key === "F") {
    setTimeout(() => {
      document.querySelector("[data-plyr=fullscreen]").click();
    }, 100);
  }
}
// register the handler
document.addEventListener("keyup", doc_keyUp);

// next and previous button function
function next() {
  let array = document.querySelectorAll(".files");
  const playing = document.querySelector(".activeColor");
  const overflw = document.querySelector(".overflw");
  let found = 0;
  for (let i = 0; i < array.length; i++) {
    if (array[i].innerText == playing.innerText) {
      found = i;
      break;
    }
  }

  array[found + 1].click();
  playing.scrollIntoView();
  overflw.scrollBy(10, -100);
}

function previous() {
  let array = document.querySelectorAll(".files");
  const playing = document.querySelector(".activeColor");
  const overflw = document.querySelector(".overflw");
  let found = 0;
  for (let i = 0; i < array.length; i++) {
    if (array[i].innerText == playing.innerText) {
      found = i;
      break;
    }
  }

  array[found - 1].click();
  playing.scrollIntoView();
  overflw.scrollBy(50, -200);
}

function showPdf(src) {
  const video = document.querySelector("video");
  video.pause();
  let res = confirm("This is a Document.Play Next Video?");
  if (res) {
    next();
  } else {
    window.open(src);
  }
}

//search bar
const searchInput = document.querySelector(".search-input");
const searchResults = document.querySelector(".search-results");

searchInput.addEventListener("input", function (event) {
  searchResults.innerHTML = "";

  let searchTerm = event.target.value.toLowerCase();
  let allFiles = document.querySelectorAll(".files");

  if (!searchTerm) {
    searchResults.style.display = "none";
    return;
  }

  for (let file of allFiles) {
    let fileName = file.textContent.toLowerCase();
    if (fileName.includes(searchTerm)) {
      let result = document.createElement("p");
      result.innerHTML = file.innerHTML;
      result.addEventListener("click", function () {
        playModule(file);
        searchResults.style.display = "none";
      });
      searchResults.appendChild(result);
    }
  }

  searchResults.style.display = "block";
});

//manually added



'''

html = '''

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <script
      src="https://kit.fontawesome.com/4518a9ec8f.js"
      crossorigin="anonymous"
    ></script>
    <link rel="stylesheet" href="https://cdn.plyr.io/3.7.3/plyr.css" />
    <link rel="stylesheet" href="./css/style.css" />
    <link
      rel="shortcut icon"
      href="https://cdn-icons-png.flaticon.com/512/4406/4406319.png"
      type="image/x-icon"
    />

    <title>Complete the Course!</title>
  </head>

  <body>
    <!-- navbar  start -->
    <nav class="nav">
      <div class="brand-area container">
        <a href="index.html" class="brand">
          <img
            src="https://beaconit.org/wp-content/uploads/2022/09/website-logologo.png"
            alt="hamidthedev Logo"
          />
        </a>
      </div>
      <div class="avatar">
        <img
          src="https://beaconit.org/wp-content/uploads/2022/09/Circle.png"
          alt="Hamidthedev Logo"
        />
        <p>HC</p>
      </div>
    </nav>
    <!-- navbar end start -->

    <!-- main start -->
    <section class="main">
      <!-- course details start -->
      <div class="milestoneDetails">
        <img
          class="milestoneImage"
          src="https://beaconit.org/wp-content/uploads/2022/09/Thumbnail_.png"
          alt=""
        />

        <video
          src=""
          class="video"
          id="player"
          playsinline
          controls
          autoplay
          data-poster="/path/to/poster.jpg"
        >
          <!-- viedo will play here-->
        </video>
        <iframe src="" class="pdf" frameborder="0"></iframe>
        <h1 class="title">Welcome to the Course!</h1>
        <!-- <p class="details">Module description here</p> -->
        <div class="playNext">
          <button class="previous" onclick="previous()">Previous</button>
          <button class="next" onclick="next()">Next</button>
        </div>
      </div>
      <!-- course details end -->

      <!-- all milestones & modules start -->
      <div style="position: relative;">
        <div class="search-container">
          <input class="search-input" type="text" placeholder="Search" />
        </div>
        <div class="search-results"></div>
        <div class="milestones">
          <div class="milestone border-b">
            <div class="flex">
              <div class="checkbox"><input type="checkbox" /></div>
              <div>
                <p>
                  Milestone 1 name
                  <span><i class="fas fa-chevron-down"></i></span>
                </p>
              </div>
            </div>
            <div class="hidden_panel">
              <div class="module border-b">
                <p>Module Name</p>
              </div>
            </div>
          </div>
        </div>
        <div class="doneList">
          <!-- done list will load here -->
        </div>
      </div>
      <!-- all milestones and modules end -->
    </section>

    <!-- <script src="./js/data.js"></script> -->
    <script src="https://cdn.plyr.io/3.7.3/plyr.polyfilled.js"></script>
    <script src="./js/main.js"></script>
    <script>
      const player = new Plyr("#player");
    </script>
  </body>
</html>


'''

css = '''
@import url("https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap");


/* input box */
.search-container{
  background-color: #150f2d;
  padding: 5px;
  border-radius: 5px;
  -webkit-border-radius: 5px;
  -moz-border-radius: 5px;
  -ms-border-radius: 5px;
  -o-border-radius: 5px;
}


.search-input {
  width: 100%;
  padding: 8px 24px;
  background-color: transparent;
  /* background-color: #212936; */
  transition: transform 250ms ease-in-out;
  font-size: 14px;
  line-height: 18px;
  color: #ffffff;
  background-color: transparent;
background-image: url("https://icons.veryicon.com/png/o/system/super-system-icon/search-153.png");
  background-repeat: no-repeat;
  background-size: 15px 15px;
  background-position: 95% center;
  border-radius: 10px;
  border: 1px solid #ffffff2b;
  transition: all 250ms ease-in-out;
  backface-visibility: hidden;
  transform-style: preserve-3d;
  -webkit-border-radius: 10px;
  -moz-border-radius: 10px;
  -ms-border-radius: 10px;
  -o-border-radius: 10px;
}

.search-input:hover,
.search-input:focus {
  padding: 9px 8px;
  outline: 0;
  border: 1px solid transparent;
  border-bottom: 1px solid #575756;
  border-radius: 0;
  background-position: 98% center;
}

/* input results shown here */
.search-results{
  position: absolute;
  left: 3px;
  margin-top: 2px;
  background: #141722;
  border-radius: 10px;
  -webkit-border-radius: 10px;
  -moz-border-radius: 10px;
  -ms-border-radius: 10px;
  -o-border-radius: 10px;
  padding: 5px;
  border: 1px solid rgba(255, 255, 255, 0.264);
  z-index: 9999;
  max-height: 50vh;
  overflow-x: auto;
  display:none;
}

.search-results p{
  margin: 5px 0;
  border-radius: 3px;
  -webkit-border-radius: 3px;
  -moz-border-radius: 3px;
  -ms-border-radius: 3px;
  -o-border-radius: 3px;
  padding: 2px;
  cursor: pointer;
}


:root {
  --lightDark: #212936;
  --dark: #141722;
  --fontPrimary: #fff;
  --green: #35bb78;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  color: var(--fontPrimary);
  font-family: "Montserrat", sans-serif;
}
body {
  position: fixed;
}

i {
  font-size: 20px;
  background: -webkit-linear-gradient(#ff3e8a, #cd52fb);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.folder {
  position: relative;
  overflow: hidden;
  cursor: pointer;
  margin: 5px 0;
  padding: 10px 10px;
  border-radius: 5px;
  background-color: #150f2d;
  -webkit-border-radius: 5px;
  -moz-border-radius: 5px;
  -ms-border-radius: 5px;
  -o-border-radius: 5px;
  /*border-bottom: 0.3px solid #555;
    */
}
.nested-folder {
  display: none;
  margin-left: 20px;
}


.nested-folder .folder{
 background-color: rgb(15, 11, 39);
}


.fa-caret-down, .fa-caret-right{
  position: absolute;
  right: 15px;
}

.files {
  overflow: hidden;
  cursor: pointer;
  margin: 5px 0;
  padding: 7px 5px;
}

body {
  background-color: var(--lightDark);
}

/* nav start */
.nav {
  background-color: var(--dark);
  padding: 15px 30px;
  display: flex;
  justify-content: space-between;
}

.nav img {
  width: 200px;
}

.avatar {
  display: flex;
  align-items: center;
  justify-content: center;
}

.nav .avatar img {
  width: 30px;
  height: 30px;
}

.avatar p {
  margin-left: 10px;
  font-size: 14px;
  color: var(--white);
}

/* Main body with grid start */
.main {
  display: grid;
  grid-template-columns: 2.3fr 1fr;
  grid-gap: 20px;
  padding: 30px;
}

.flex {
  display: flex;
}

.checkbox {
  width: 40px;
}

.milestoneDetails img {
  width: 100%;
  height: auto;
  object-fit: cover;
  border-radius: 7px;
  -webkit-transition: opacity 0.8s linear;
  -moz-transition: opacity 0.8s linear;
  transition: opacity 0.8s linear;
}

.title,
.details {
  margin: 10px auto;
  padding: 5px 10px;
  margin-right: 30vw;
}

.milestones,
.doneList {
  /* background-color: var(--dark); */
  border-radius: 7px;
  cursor: pointer;
  max-height: 65vh;
  overflow: auto;
}

.doneList {
  margin-top: 20px;
}

.module {
  background-color: var(--dark);
}

.milestone,
.module {
  font-size: 14px;
  color: var(--white);
  margin: 10px;
  padding: 10px;
}

.milestoneDetails {
  font-size: 14px;
  color: var(--white);
}

.border-b {
  border-bottom: 1px solid rgb(31, 41, 55);
}

.hidden_panel {
  max-height: 0;
  overflow: hidden;
  -webkit-transition: max-height 0.8s;
  -moz-transition: max-height 0.8s;
  transition: max-height 0.8s;
}

.active {
  font-weight: bold;
}

.show {
  max-height: 400px;
}

.loaded {
  opacity: 1;
}

input[type="checkbox"] {
  margin-right: 5px;
  vertical-align: middle;
}

#player {
  display: none;
  width: 100%;
  height: auto;
  object-fit: cover;
  border-radius: 7px;
  -webkit-transition: opacity 0.8s linear;
  -moz-transition: opacity 0.8s linear;
  transition: opacity 0.8s linear;
}

.activeColor {
  background: #6333f0;
  border-radius: 5px;
  -webkit-border-radius: 5px;
  -moz-border-radius: 5px;
  -ms-border-radius: 5px;
  -o-border-radius: 5px;
}

.playNext button {
  cursor: pointer;
  background: none;
  margin: 10px auto;
  margin-left: 10px;
  padding: 10px 80px;
  border-radius: 50px;
  border: 1px solid white;
  -webkit-border-radius: 50px;
  -moz-border-radius: 50px;
  -ms-border-radius: 50px;
  -o-border-radius: 50px;
}

.next {
  border: 1px solid #ff3e8a !important;
  background: #ff3e8a !important;
}

.pdf {
  display: none;
  width: 100%;
}

.overflw {
  overflow-y: scroll;
}

/* scrollbar design  */
::-webkit-scrollbar {
  width: 12px;
}

/* Track */
::-webkit-scrollbar-track {
  background: none;
}

/* Handle */
::-webkit-scrollbar-thumb {
  height: 15%;
  background: rgb(67, 71, 85);
  border-radius: 10px;
  -webkit-border-radius: 10px;
  -moz-border-radius: 10px;
  -ms-border-radius: 10px;
  -o-border-radius: 10px;
}

/* Handle on hover */
::-webkit-scrollbar-thumb:hover {
  background: #555;
}

@media only screen and (max-width: 1024px) {
  .main,
  .todo {
    grid-template-columns: repeat(1, 1fr);
    padding: 15px;
    grid-gap: 10px;
  }

  .nav img {
    width: 150px;
  }

  .nav .avatar img {
    width: 20px;
    height: 20px;
  }

  .milestones,
  .doneList {
    height: fit-content;
  }

  .title {
    margin-right: 0px;
  }

  .playNext button {
    margin: 10px auto;
    margin-top: 0px;
  }
  .playNext {
    margin-top: 0;
    margin-left: 0;
  }
  .milestones {
    max-height: 18em;
  }
}


'''

# js = js_init.format(courseData=data)
try:
    os.mkdir("js")
except:
    print("Path already Exist!")
try:
    os.mkdir("css")
except:
    print("path already exist!")

jsfile = "main.js"
os.path.join("./js", jsfile)

stylefile = "style.js"
os.path.join("./css", stylefile)


with open("./js/main.js", 'wb') as file:
    file.write(courseInfo.encode())

with open("./js/main.js", 'ab') as file:
    file.write(js.encode())

with open("./css/style.css", 'wb') as file:
    file.write(css.encode())

with open("index.html", 'wb') as file:
    file.write(html.encode())

time.sleep(1)
print("Just double click on 'Index.html!'")
