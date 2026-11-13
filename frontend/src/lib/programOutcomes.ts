export type ProgramLearningOutcome = {
  code: string;
  title: string;
  statement: string;
};

export type ProgramEducationalObjective = {
  code: string;
  statement: string;
};

/**
 * The three approved Program Educational Objectives.
 *
 * From the same document as the outcomes below, and carried across under the
 * same rule: the wording is the document's. Unlike the PLOs these carry no
 * short name of their own, only a numbered statement, so none is invented for
 * them here.
 */
export const programEducationalObjectives: ProgramEducationalObjective[] = [
  {
    code: "PEO1",
    statement:
      "To prepare graduates with mechanical engineering competencies to solve workplace problems while upholding professional ethics.",
  },
  {
    code: "PEO2",
    statement:
      "To prepare graduates to protect human well-being and the environment, contributing to sustainable development.",
  },
  {
    code: "PEO3",
    statement:
      "To prepare graduates to continuously develop their competencies in order to keep pace with rapid technological advancement and globalization.",
  },
];

/**
 * The ten approved Program Learning Outcomes.
 *
 * Transcribed from the Mechanical Engineering program development document.
 * These are accreditation statements, so the wording is the document's and not
 * ours: it is not edited for house style, tightened, or re-ordered. The only
 * changes are sentence capitalisation where the source runs a lower-case verb
 * on from the colon, and British spelling left exactly as the document has it.
 *
 * Held here rather than in Wagtail because they change when the program is
 * revalidated rather than when someone fancies a rewrite, and a static file
 * keeps them identical to the approved document until that happens.
 */
export const programLearningOutcomes: ProgramLearningOutcome[] = [
  {
    code: "PLO1",
    title: "Scientific and Technical Knowledge",
    statement:
      "Understand the basic scientific and technical knowledge within mechanical discipline, organize and integrate theories, principles, as well as methods to recognize and solve the problem.",
  },
  {
    code: "PLO2",
    title: "Apply Sciences, Mathematics, and Computer for Problem Solving Skill",
    statement:
      "Apply concepts, principles, theories of science and mathematics with computer to analyse and evaluate problems or tasks, especially when faced with unfamiliar or complex situations, and to develop creative solutions using logical reasoning and systematic thinking.",
  },
  {
    code: "PLO3",
    title: "Machines and Tools Proficiency",
    statement:
      "Perform mechanical tool and machine by combining multiple skills in sequence, reproducing them precisely, and executing them consistently with minimal effort.",
  },
  {
    code: "PLO4",
    title: "Interpersonal Skill",
    statement:
      "Establish and enhance personal and work-based relationships characterized by effective communication and conflict resolution.",
  },
  {
    code: "PLO5",
    title: "Responsibility",
    statement:
      "Take responsibility for their own learning and continuing personal and professional development, work effectively in group and exercise leadership when appropriate, act responsibly in personal and professional relationship.",
  },
  {
    code: "PLO6",
    title: "Entrepreneurial Skill",
    statement:
      "Transform creativity into innovation, identify opportunities, generate solutions, and navigate uncertainty.",
  },
  {
    code: "PLO7",
    title: "Ethics and Professionalism",
    statement:
      "Identify technical issues, make ethical decisions, and act professionally within diverse social and professional environments, considering local and global issues related to science, technology, business, and the environment.",
  },
  {
    code: "PLO8",
    title: "Communication",
    statement:
      "Develop effective communication by using clear, coherent, and persuasive language appropriate to the purpose and adaptable to the context, in both oral and written forms.",
  },
  {
    code: "PLO9",
    title: "Information Technology or Digital Skill",
    statement:
      "Apply information and communication technology to support work or task.",
  },
  {
    code: "PLO10",
    title: "Numerical Skill",
    statement:
      "Encode the problem and work with number in order to use mathematical and statistics techniques to solve the complex problem in mechanical discipline.",
  },
];
