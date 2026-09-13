/**
 * Sections that are built but switched off on the public site.
 *
 * A switch turns off everything that belongs to its section at once, so a
 * hidden section leaves no menu entry pointing at an anchor that is not there.
 */
export const features = {
  /**
   * The jobs and internships board: the homepage band, its header and footer
   * links, and the posting pages under /opportunities.
   *
   * Off until partner organizations are posting to it. An empty board can only
   * say that nothing is open, which a prospective student reads as "no jobs
   * for ME graduates" rather than "nothing posted yet". Postings can still be
   * prepared in Wagtail meanwhile, and appear once this is true again.
   */
  opportunities: false,
};
