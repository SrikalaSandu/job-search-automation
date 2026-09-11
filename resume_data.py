"""
This is the master copy of your resume content, in plain text, that every
job gets matched against and every tailored resume gets built from.

IMPORTANT: Update this whenever your real resume changes. The scoring and
resume-tailoring steps only know what's written here — they never invent
experience that isn't in this file.
"""

CANDIDATE_NAME = "Srikala Sandu"
CANDIDATE_EMAIL = "sandusrikala@gmail.com"
CANDIDATE_PHONE = "+1 (551) 554-1160"
CANDIDATE_LOCATION = "Jersey City, NJ"

MASTER_RESUME_TEXT = """
SRIKALA SANDU
sandusrikala@gmail.com | Jersey City, NJ | +1 (551) 554-1160

PROFESSIONAL SUMMARY
AI Engineer with 4+ years delivering production ML systems, including RAG
pipelines and computer-vision applications. Designed and benchmarked
retrieval-augmented generation pipelines that cut latency by ~30% and
authored a peer-reviewed paper on multi-modal AI for assistive technology
at ACM SIGACCESS ASSETS 2025. Proficient in Python, LangChain, OpenCV, and
cloud services.

EDUCATION
Master of Science in Computer Science, Stevens Institute of Technology,
Hoboken, NJ. GPA 3.8/4.0, Provost Scholar. Sep 2024 - May 2026.
Coursework: Deep Learning, Mathematical Foundations of Machine Learning,
Data Analytics and Statistical Methods, Advanced Algorithm Design,
Fundamentals of CyberSecurity, Human-Computer Interaction.

Bachelor of Science in Computer Science, Visveshvaraya Technology
University, Bangalore, India. GPA 7.0/10.0. Sep 2017 - Aug 2021.

SKILLS
Languages/Scripting: C, C++, Java, C#, Python, Ruby, SQL, HTML, CSS,
JavaScript, PHP, R, Bootstrap, Kotlin
Frameworks/Tools/OS: React.js, React Native, Node.js, Jupyter Notebook,
OpenGL, API Integration, Linux, Unix, Android Studio
Databases: MongoDB, Firebase
Applied ML/GenAI: PyTorch, TensorFlow, scikit-learn, XGBoost, OpenCV, NLP,
Computer Vision, Multi-Modal AI (VLMs, OCR)
Infrastructure: Docker, Kubernetes, AWS, FastAPI, CI/CD
GenAI/LLMOps: LangChain, LangGraph, LlamaIndex, Hugging Face, RAG,
Agentic Workflows, Prompt Engineering, RAGAS, DeepEval

PROFESSIONAL EXPERIENCE

Graduate Research Assistant — Stevens Institute of Technology, Hoboken, USA
Jan 2025 - July 2026
- Built an Android app using Kotlin, OpenCV 4.9, and Camera2 API for Vuzix
  M400 smart glasses that performed real-time form-field detection via
  Canny edge detection, contour analysis, and perspective warp, enabling
  users to capture and process forms on-device.
- Engineered an IoU-based spatial accuracy algorithm measuring mappability
  (87%), start-point accuracy (74%), and within-box accuracy (54%) across
  25 blind participants; conducted Likert-scale usability analysis in R,
  achieving a 68% efficiency gain.
- Authored and published a first-author peer-reviewed paper on multi-modal
  AI for assistive technology at ACM SIGACCESS ASSETS 2025.

Generative AI Engineer Intern — G5 Infotech, Remote, USA
Mar 2026 - Apr 2026
- Benchmarked 3+ RAG chunking strategies (fixed-size, semantic, recursive)
  using LangChain/Hugging Face, evaluating precision/recall/MRR, achieving
  ~30% retrieval latency reduction in production.
- Tuned Pinecone vector-DB config and context-window management, achieving
  ~22% faster average response time.

Software Developer — CircleZapp, Remote, USA
Dec 2024 - Feb 2025
- Built a This-or-That preference chatbot and a Six Degrees of Separation
  graph algorithm using NetworkX to match users by shared interests,
  location, school, and community across 10,000+ active accounts.
- Optimized graph indexing to cut average match latency from 800ms to
  340ms, delivering both features within 3 months.
- Prototyped and A/B-tested 3 collaborative filtering variants against
  live behavioral data, lifting click-through rate by 12% in holdout
  tests; findings directly shaped 2 product feature releases.

Community Developer — Reddit Inc., Bangalore, India
April 2023 - August 2024
- Built Python/YAML moderation bots on Reddit's Devvit platform for
  automated spam removal and content filtering, reducing manual
  moderation workload by 40% across a team of 8 moderators.
- Engineered Python and Reddit API-driven automation to detect spam,
  hate speech, and policy violations, achieving 92% real-time
  harmful-content identification accuracy and reducing toxic behavior
  reports by 35%.
- Authored step-by-step bot configuration guides and troubleshooting
  runbooks, cutting volunteer moderator onboarding time from ~3 weeks to
  ~10 days (a 50% reduction).

Backend Developer — Certes Networks, Bangalore, India
April 2022 - April 2023
- Engineered core C++ features for encryption hardware, including Syslog
  integration, a custom LCD Linux driver, and LM Sensors support,
  extending device monitoring and diagnostics capabilities.
- Identified and resolved a critical bug causing legacy Certes End Points
  (CEPs) to silently fail encryption, preventing undetected data exposure
  across deployed devices.
- Dockerized deployment pipelines for encryption hardware software,
  streamlining builds and improving deployment consistency.
- Refactored 5+ high-throughput backend modules, improving encryption
  efficiency by 20% while sustaining 99.8% uptime.

PUBLICATIONS
"Interactive Form Filling Assistant on Smart Glasses for Blind Users" —
S. Sandu, R. R. Khan, J. Hong. ACM SIGACCESS Conference on Computers and
Accessibility (ASSETS), October 2025. https://doi.org/10.1145/3663547.3759722
[This publication must always appear as its own section on any tailored
resume, regardless of role.]

PROJECTS
- Stock Trend Forecasting: end-to-end ML pipeline achieving 85% prediction
  accuracy; XGBoost, Random Forests, scikit-learn, time-series
  cross-validation.
- AI College Admission Chatbot: NLP-powered chatbot, 95% query accuracy,
  40% efficiency increase in admissions inquiries.
- MindMate: LLM-powered backend on Firebase generating adaptive daily
  action plans; ElevenLabs voice interaction for goal coaching.
- WYR Chatbot: NLP-based conversational chatbot; adapted for a therapy
  research assistant use case.

CERTIFICATIONS
Agentic AI Fundamentals: Architectures, Frameworks & Applications; OpenAI
API: Agents; Building Agents with the Google Agent Developer Kit;
Hands-On AI: Building AI Agents with MCP and Agent2Agent (A2A); Build AI
Agents and Chatbots with LangGraph; Multimodal AI Essentials; PyTorch
Essential Training: Deep Learning; Claude with Amazon Bedrock by
Anthropic; AWS Certified AI Practitioner (AIF-C01) Cert Prep; AWS
Certified Generative AI Developer - Professional (AIP-C01) Cert Prep; AWS
Certified Machine Learning Engineer Associate (MLA-C01) Cert Prep; AWS
Certified Data Engineer Associate (DEA-C01) Cert Prep.

RESUME FORMATTING RULES (apply when generating a tailored resume)
- One page only.
- Arial font throughout, all text black (no color, no blue links in body).
- No bold or italics inside bullet text — bold is reserved for name,
  section headers, and job title/location lines.
- Bold job title + location on one line; plain org name + dates on the
  next line.
- Bold skill category labels (e.g. "Applied ML/GenAI:") followed by plain
  text values.
- Full degree titles spelled out: "Master of Science in Computer Science",
  "Bachelor of Science in Computer Science".
- The ACM SIGACCESS ASSETS 2025 publication is always its own section,
  never folded into Experience or Projects.
"""
