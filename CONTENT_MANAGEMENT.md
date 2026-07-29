# ME Website Content Management

The website content is managed through Wagtail. While developing locally, open:

- Website: `http://127.0.0.1:3000`
- CMS: `http://127.0.0.1:8000/admin/`

For the deployed website, open:

- CMS: `https://me-api.putsaccada.dpdns.org/admin/`

## Where to edit each part of the website

Sign in to the CMS, then use these sections:

| Website content | CMS location |
| --- | --- |
| Hero headline, description, vision, mission, program years, credits, contact information, social links and application link | **Settings** -> **Program settings** |
| The nine "Why choose ME" cards | **Snippets** -> **Why choose ME items** |
| Homepage focus cards and each focus-page title, introduction, image and colour | **Snippets** -> **Focus areas** |
| Learning outcomes, learning activities and career cards on each focus page | **Snippets** -> **Focus area details** |
| Equipment cards on focus pages | **Snippets** -> **Facilities** |
| Curriculum year headings and descriptions | **Snippets** -> **Curriculum years** |
| Course rows on the homepage and focus pages | **Snippets** -> **Courses** |
| Research cards | **Snippets** -> **Research projects** |
| Partner logos and partner types | **Snippets** -> **Partners** |
| Jobs, internships, scholarships and training announcements | **Snippets** -> **Opportunities** |
| Faculty and staff profiles on the People page | **Snippets** -> **Faculty members** |
| News, open houses, seminars and events | **Snippets** -> **News events** |

Use **Sort order** to control the order of cards. Lower numbers appear first.
The same focus-area, course, facility and research records are reused on the
homepage and focus subpages, so one CMS update keeps both locations consistent.

Section headings such as "Nine reasons", "Areas of focus" and "Applied
research" are currently part of the frontend design rather than CMS records.
They can be changed in the source code, or moved into Program settings in a
future CMS enhancement if non-technical editors need to revise them often.
The introductory Alumni section is also design copy for now; individual alumni
profiles will need a dedicated CMS content type before they can be managed like
faculty profiles.

## Edit the main navigation

The main navigation is stored in one frontend configuration file:

`frontend/src/config/navigation.ts`

Each top-level object in `navigationItems` is one navigation section. The order
of those objects controls the left-to-right order in the desktop header and the
top-to-bottom order in the mobile menu.

To add a section, add another object:

```ts
{
  label: "New Section",
  links: [
    { label: "First Page", href: "/first-page" },
    { label: "Second Page", href: "/second-page" },
  ],
},
```

To remove a section or subsection, remove its matching object. To reorder
sections or links, move the complete object higher or lower in its array.

For a two-level submenu, use `children`:

```ts
{
  label: "Research Area",
  children: [
    { label: "DMP", href: "/focus/design-and-manufacturing-process" },
    { label: "TES", href: "/focus/thermofluid-and-energy-system" },
  ],
},
```

Internal links begin with `/`. To link to a specific section on a page, append
its HTML anchor, for example `/about#vision`. Every navigation item must have
either an `href` or a `children` array.

Navigation is currently source-controlled rather than managed in Wagtail. This
keeps structural site changes reviewed and versioned. A Wagtail navigation
editor can be added later if program administrators need to change the menu
without deploying the frontend.

If no administrator account exists, create one from the `backend` directory:

```powershell
.\.venv\Scripts\python.exe src\manage.py createsuperuser
```

## Add or replace a machine image

1. Sign in to the CMS.
2. Open **Images** and select **Add an image**.
3. Upload the machine photograph and give it a clear title.
4. Open **Snippets** → **Facilities**.
5. Select the machine, choose the uploaded image in the **Image** field, and save.
6. Confirm that the correct **Focus areas** are selected.

Recommended machine-image preparation:

- Landscape 3:2 composition, ideally around `1500 × 1000 px`.
- JPG or WebP for photographs; keep the file near or below 1.5 MB when practical.
- Place the machine near the centre because the website crops the edges on smaller screens.
- Avoid adding captions or important text inside the photograph.
- Use a descriptive image title, for example `DMP — SYIL X9 5-Axis Machining Center`.

Uploaded source images are stored under `backend/src/media/` in the default local setup. Back up that folder together with the database. Do not commit uploaded media to Git.

## Enter the official curriculum

### 1. Configure each academic year

Open **Snippets** → **Curriculum years** and edit Year 1 through Year 4.

- **Sort order:** `1`, `2`, `3`, or `4`.
- **Year:** academic year number.
- **Theme:** the short headline displayed in the curriculum panel.
- **Credit count:** the official total credits for that year.
- **Description:** a concise explanation of the year's learning purpose.

### 2. Add the courses

Open **Snippets** → **Courses** and add or edit every course.

- **Sort order:** controls the order shown within the year.
- **Curriculum year:** links the course to Year 1, 2, 3, or 4.
- **Code:** official subject code; it must be unique within that year.
- **Title:** official subject name.
- **Credits:** official credit value.
- **Semester:** Semester 1, Semester 2, or Full year.
- **Focus areas:** select DMP, TES, MAS, or ECM when the course directly supports that focus.

The homepage shows courses grouped by curriculum year. Each focus-area page shows only courses mapped to that focus area, so the **Focus areas** field is important.

After saving, refresh the frontend page. The frontend requests live CMS content and does not cache these records.

## Important content safety note

`seed_me_content` is intended for initial sample content. After replacing the sample curriculum with the official program data, do not run the seed command again unless you have first reviewed how it will update existing records.

For a large curriculum, prepare a spreadsheet with these columns and import it in one batch rather than entering every course manually:

`year, year_theme, year_credit_count, year_description, sort_order, course_code, course_title, course_credits, semester, focus_areas`
