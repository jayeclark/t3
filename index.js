import { getKey } from './get.js';

process.env = (key) => getKey(key);

const extractBody = (str) => {
  let start = str.search(/<body>/) + 6;
  let end = str.search(/<\/body>/);
  return str.substring(start, end);
}

const checkAnswer = (event) => {
  let answerId = event.target.id.split('-');
  let button = document.getElementById(event.target.id);
  let index = questions.findIndex(q => Number(q.id) === Number(answerId[0]));
  let {correct_answers} = questions[index];
  if (correct_answers[answerId[1]] == 'true') {
      correct[index] = true;
      button.classList.add("btn-success");
      button.classList.remove("btn-light");
  } else {
      button.classList.add("btn-danger");
      button.classList.remove("btn-light");
  }
}

const reload = () => {
  questions = [];
  correct = [];
  document.getElementById("questions").innerHTML = "";
  document.getElementById("input-wrapper").style.display = "";
  document.getElementById("input-intro").style.display = "";

  const button = document.getElementById('start-stop');
  button.classList.add("btn-success");
  button.classList.remove("btn-warning");
  button.classList.remove("btn-danger");
  button.innerHTML = "Start Quiz";
  button.removeEventListener('click', reload);
  button.addEventListener('click', loadQuestions);
}

const displayQuestions = (arr) => {
  const element = document.getElementById("questions");
  const heading = document.createElement("h1");
  heading.style.color = "rgb(100, 176, 67)";
  heading.style.marginTop = "30px";
  heading.innerHTML = `${page} Quiz`;
  element.append(heading);
  const inner = arr.map((q) => {
      let answers = Object.keys(q.answers);
      let filtered_answers = answers.filter(a => q.answers[a] !== null);

      let wrapper = document.createElement('div', { id: q.id});

      wrapper.classList.add("question");
      let question = document.createElement('p');
      question.style.fontWeight = "600";
      question.innerHTML = q.question.replace(/</g,"&lt;").replace(/>/g,"&gt;");
      wrapper.appendChild(question);

      filtered_answers.forEach(a => {
          let button = document.createElement('button', {id: `${q.id}-${a}_correct`, type: "button", onClick: (e) => checkAnswer(e)});
          button.id = `${q.id}-${a}_correct`;
          button.type = "button";
          button.addEventListener('click', (e) => checkAnswer(e));
          button.style.fontSize = "0.9rem";
          button.style.margin = "8px";

          button.innerHTML = q.answers[a].replace(/</g,"&lt;").replace(/>/g,"&gt;");
          button.classList.add("btn");
          button.classList.add("btn-light");
          wrapper.appendChild(button);
      })
      return wrapper;
  });
  inner.forEach(innerChild => {
      const hRule = document.createElement('hr');
      element.appendChild(hRule);
      element.appendChild(innerChild);
  })
}



const loadQuestions = async () => {
  const button = document.getElementById('start-stop');
  button.classList.add("btn-warning");
  button.classList.remove("btn-success");
  button.innerHTML = "Loading Questions";
  button.removeEventListener('click', loadQuestions);
  questions = await superagent
      .get('https://quizapi.io/api/v1/questions')
      .query({
          category: formValues.category,
          difficulty: formValues.difficulty,
          limit: formValues.number
      })
      .set('X-API-Key', process.env('apiKey'))
      .set('Accept', 'application/json')
      .then(res => {
          return res.body;
          });
  document.getElementById("input-wrapper").style.display = "none";
  document.getElementById("input-intro").style.display = "none";
  displayQuestions(questions);
  button.innerHTML = "New Quiz";
  button.addEventListener('click', reload);
}

window.onload = (async () => {
  const button = document.getElementById("start-stop");
  if (button) button.addEventListener('click', loadQuestions);

  let header = await fetch('navbar.html');
  let headerText = await header.text();
  document.querySelector('#header').innerHTML = extractBody(headerText);
  document.querySelector(`#${page.toLowerCase()}-page`).classList.add("active");

  let footer = await fetch('footer.html');
  let footerText = await footer.text();
  document.querySelector('#footer').innerHTML = extractBody(footerText);

})