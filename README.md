# GSU-Registration

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Swifty</h3>

  <p align="center">
    The revolution of registration at Grambling State University!
    <br />
    <a href=""><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/othneildrew/Best-README-Template">View Demo</a>
    &middot;
    <a href="https://github.com/othneildrew/Best-README-Template/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://github.com/othneildrew/Best-README-Template/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>




The ultimate web app designed to simplify the course selection and registration process at Grambling State University.

<p align="center">
  <img src="images/logo.png" alt="GSU-Registration Logo" width="80" height="80">
</p>

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#key-benefits">Key Benefits</a></li>
    <li><a href="#technologies-used">Technologies Used</a></li>
    <li><a href="#key-features">Key Features</a></li>
    <li><a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

---

## About The Project

GSU-Registration is a one-stop web application that streamlines course selection and registration for Grambling State University students. By centralizing access to academic history, required courses, and class listings, it removes the administrative burden so students can focus on learning.

---

## Key Benefits

- **Time Efficiency:** Automates and accelerates the registration workflow.  
- **Centralized Systems:** No more hopping between Banner, DegreeWorks, and gram.edu.  
- **Personalized Experience:** Generates timetables tailored to each student’s preferences.  
- **User-Friendly Interface:** Intuitive design built with students in mind.

---

## Technologies Used

### Built With
* ![Python][python]
* ![Selenium][selenium] ![Flask][flask]
* ![AWS][aws] &nbsp; ![MySQL][mysql]
* ![HTML5][html5] &nbsp;&nbsp; ![CSS3][css3] &nbsp;&nbsp; ![Bootstrap][Bootstrap]


---

## Key Features

1. **Data Aggregation**  
   Pulls academic information from Banner Web, gram.edu, and DegreeWorks into a unified dashboard.  
2. **Direct Input Capabilities**  
   Seamlessly posts selections back to external systems, reducing manual entry.  
3. **Personalized Timetables**  
   Analyzes degree requirements and past coursework to build your optimal schedule automatically.

---

## Getting Started

Follow these instructions to run GSU-Registration locally.

### Prerequisites

- Python 3.8+  
- MySQL Server  
- `pip` package manager  

### Installation

1. **Clone the repo**
   ```bash
   git clone https://github.com/<your-username>/GSU-Registration.git
   cd GSU-Registration
   ```
2. **Create & activate a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate    # on Windows use `venv\Scripts\activate`
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure your database**  
   Create a `.env` file in the project root with your MySQL credentials and any secret keys.
5. **Run the application**
   ```bash
   flask run
   ```
6. **Open your browser**  
   Navigate to `http://localhost:5000` to begin.

---

## Roadmap

- [x] Data aggregation from Banner, gram.edu, DegreeWorks  
- [x] Automated timetable generation  
- [ ] Mobile-friendly UI  
- [ ] Advanced “what-if” scheduling scenarios  
- [ ] Notification integration (email/SMS reminders)

---

## Contributing

Contributions are welcome! To propose a change:

1. Fork this repository.  
2. Create a feature branch (`git checkout -b feature/MyFeature`).  
3. Commit your changes (`git commit -m "Add MyFeature"`).  
4. Push to your branch (`git push origin feature/MyFeature`).  
5. Open a Pull Request.

---

## Contact

Your Name - [@your_twitter](https://twitter.com/your_username) - email@example.com
Project Link: [https://github.com/your_username/repo_name](https://github.com/your_username/repo_name)
<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## License

Distributed under the Unlicense. See `LICENSE` for more information.

---

## Acknowledgments

* [Flask Documentation](https://flask.palletsprojects.com/)  
* [Selenium Official Site](https://www.selenium.dev/)  
* [AWS Docs](https://docs.aws.amazon.com/)  
* [MDN Web Docs](https://developer.mozilla.org/)  
* [Img Shields](https://shields.io/)

  
<!-- badge definitions -->
[python]:       https://img.shields.io/badge/Python-3776AB.svg?style=for-the-badge&logo=python&logoColor=white
[selenium]:     https://img.shields.io/badge/Selenium-43B02A.svg?style=for-the-badge&logo=selenium&logoColor=white
[swift]:        https://img.shields.io/badge/Swift-FA7343.svg?style=for-the-badge&logo=swift&logoColor=white
[cpp]:          https://img.shields.io/badge/C%2B%2B-00599C.svg?style=for-the-badge&logo=c%2B%2B&logoColor=white

[aws]:          https://img.shields.io/badge/Amazon%20AWS-232F3E.svg?style=for-the-badge&logo=amazonaws&logoColor=white
[flask]:        https://img.shields.io/badge/Flask-000000.svg?style=for-the-badge&logo=flask&logoColor=white
[vscode]:       https://img.shields.io/badge/VS%20Code-007ACC.svg?style=for-the-badge&logo=visualstudiocode&logoColor=white
[xcode]:        https://img.shields.io/badge/Xcode-147EFB.svg?style=for-the-badge&logo=xcode&logoColor=white

[mysql]:        https://img.shields.io/badge/MySQL-4479A1.svg?style=for-the-badge&logo=mysql&logoColor=white
[postgresql]:   https://img.shields.io/badge/PostgreSQL-336791.svg?style=for-the-badge&logo=postgresql&logoColor=white
[mongodb]:      https://img.shields.io/badge/MongoDB-47A248.svg?style=for-the-badge&logo=mongodb&logoColor=white
[html5]:        https://img.shields.io/badge/HTML5-E34F26.svg?style=for-the-badge&logo=html5&logoColor=white
[css3]:         https://img.shields.io/badge/CSS3-1572B6.svg?style=for-the-badge&logo=css3&logoColor=white
[Bootstrap]:    https://img.shields.io/badge/Bootstrap-563D7C.svg?style=for-the-badge&logo=bootstrap&logoColor=white

