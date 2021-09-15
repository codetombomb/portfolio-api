Technology.destroy_all
Project.destroy_all

technologies = [
  "Javascript",
  "Ruby on Rails",
  "HTML",
  "CSS",
  "React",
  "Ruby",
  "Active Record",
]

technologies.each do |tech|
  Technology.create(name: tech)
end

cc = Project.create(
  title: "Covid Chaos",
  description: "Covid Chaos was my Mod 3 project at Flatiron School. It was the end of February 2020 when Flatiron School and many other schools sent thier students to work from home and self isolate. Toilet paper, and other essential items like hand sanitizer, became scarce as well as decency during the uncertain times. I knew I wanted to create a game for the project and thought that it would be a good distraction, to the madness unfolding around me, to tie the theme of the game to the chaos.",
  img_name: "covid_chaos",
  youtube_link: "https://youtu.be/gVurgKxb6l8",
  github_link: "https://github.com/codetombomb/covid-chaos-frontend",
)

ProjectTechnology.create(project_id: cc.id, technology_id: 1)
ProjectTechnology.create(project_id: cc.id, technology_id: 2)

jeopardy = Project.create(
  title: "This is Jeopardy",
  description: "This is a command line prompt game that will allow the user to select a category and value and the user will choose the correct answer from a list of options. The user can create a username and password when they start the game. The game will keep track of the score and save their highest score to the user's account.",
  img_name: "jeopardy",
  youtube_link: "https://youtu.be/YuLM-0J_7k8",
  github_link: "https://github.com/codetombomb/this_is_jeopardy",
)

ProjectTechnology.create(project_id: jeopardy.id, technology_id: 6)
ProjectTechnology.create(project_id: jeopardy.id, technology_id: 7)

react_tarot = Project.create(
  title: "ReacTarot",
  description: "ReacTarot is a React demo that can be used to teach the core concepts of React including: \n * Props \n * Container components \n * Conditional rendering \n * Filtering \n * State \n * Event hanlding \n * Rendering components for each element in array \n * Lifecycle events \n * Function components \n * Class components",
  img_name: "reacTarot",
  youtube_link: "https://youtu.be/DAiSeFH4b4U",
  github_link: "https://github.com/codetombomb/react-tarot-lab",
)

ProjectTechnology.create(project_id: react_tarot.id, technology_id: 3)
ProjectTechnology.create(project_id: react_tarot.id, technology_id: 4)
ProjectTechnology.create(project_id: react_tarot.id, technology_id: 5)

traits = [
  "father",
  "husband",
  "programmer",
  "motorbikes",
  "creative",
  "learner",
  "foodie",
  "music",
]

traits.each do |trait|
    AboutMe.create(trait: trait)
end