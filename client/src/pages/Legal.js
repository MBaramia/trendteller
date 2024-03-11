import "./Tutorial.css";
import SummaryTextView from "../components/SummaryTextView";

function Legal() {
  const terms = (
    <span>
      Last updated: 11/03/2024 <br />
      <br />
      Please read these Terms and Conditions ("Terms", "Terms and Conditions")
      carefully before using the Trendteller website operated by group 11 of
      CS261: software engineering (Jayesh, Josia, Mohammed, Rushen, Saahil)
      ("us", "we", or "our"). <br />
      <br />
      Your access to and use of the Service is conditioned on your acceptance of
      and compliance with these Terms. These Terms apply to all visitors, users
      and others who access or use the Service.
      <br />
      <br />
      By accessing or using the Service you agree to be bound by these Terms. If
      you disagree with any part of the terms then you may not access the
      Service.
      <br />
      <br />
      Links To Other Websites:
      <br />
      <br />
      Our Service may contain links to third-party web sites or services that
      are not owned or controlled by group 11.
      <br />
      <br />
      Group 11 has no control over, and assumes no responsibility for, the
      content, privacy policies, or practices of any third party web sites or
      services. You further acknowledge and agree that group 11 shall not be
      responsible or liable, directly or indirectly, for any damage or loss
      caused or alleged to be caused by or in connection with use of or reliance
      on any such content, goods or services available on or through any such
      web sites or services.
      <br />
      <br />
      Termination:
      <br />
      <br />
      We may terminate or suspend access to our Service immediately, without
      prior notice or liability, for any reason whatsoever, including without
      limitation if you breach the Terms.
      <br />
      <br />
      All provisions of the Terms which by their nature should survive
      termination shall survive termination, including, without limitation,
      ownership provisions, warranty disclaimers, indemnity and limitations of
      liability.
      <br />
      <br />
      Changes:
      <br />
      <br />
      We reserve the right, at our sole discretion, to modify or replace these
      Terms at any time. If a revision is material we will try to provide at
      least 30 days' notice prior to any new terms taking effect. What
      constitutes a material change will be determined at our sole discretion.
      <br />
      <br />
      Contact Us:
      <br />
      <br />
      If you have any questions about these Terms, please contact us.
    </span>
  );

  const privacy = (
    <span>
      Last updated: 11/03/2024
      <br />
      <br />
      Definitions:
      <br />
      <br />
      ● Trendteller
      <br />
      <br /> Trendteller means the Trendteller website, run by group 11 of
      CS261: software engineering (Jayesh, Josia, Mohammed, Rushen, Saahil).
      <br />
      <br />
      ● GDPR
      <br />
      <br /> General Data Protection Regulation Act.
      <br />
      <br />
      ● Data Controller
      <br />
      <br /> Data Controller means the natural or legal person who (either alone
      or jointly or in common with other persons) determines the purposes for
      which and the manner in which any personal information is, or is to be,
      processed.
      <br />
      <br />
      ● Data Processor
      <br />
      <br /> Data Processor means any natural or legal person who processes the
      data on behalf of the Data Controller.
      <br />
      <br />
      ● Data Subject
      <br />
      <br /> Data Subject is any living individual who is using our Service and
      is the subject of Personal Data.
      <br />
      <br />
      1. Principles for processing personal data
      <br />
      <br />
      Our principles for processing personal data are:
      <br />
      <br />
      ● Fairness and lawfulness. When we process personal data, the individual
      rights of the Data Subjects must be protected. All personal data must be
      collected and processed in a legal and fair manner.
      <br />
      <br />
      ● Restricted to a specific purpose. The personal data of Data Subject must
      be processed only for specific purposes.
      <br />
      <br />
      ● Transparency. The Data Subject must be informed of how his/her data is
      being collected, processed and used.
      <br />
      <br />
      2. What personal data we collect and process
      <br />
      <br />
      Trendteller collects several different types of personal data for various
      purposes. Personal Data may include, but is not limited to:
      <br />
      <br />
      ● Email address
      <br />
      <br />
      3. How we use the personal data
      <br />
      <br />
      Trendteller uses the collected personal data for various purposes:
      <br />
      <br />
      ● To provide you with services
      <br />
      <br />
      ● To detect, prevent and address technical issues
      <br />
      <br />
      4. Legal basis for collecting and processing personal data
      <br />
      <br />
      Trendteller legal basis for collecting and using the personal data
      described in this Data Protection Policy depends on the personal data we
      collect and the specific context in which we collect the information:
      <br />
      <br />
      ● Trendteller needs to perform a contract with you
      <br />
      <br />
      ● You have given Trendteller permission to do so
      <br />
      <br />
      ● Processing your personal data is in Trendteller legitimate interests
      <br />
      <br />
      ● Trendteller needs to comply with the law
      <br />
      <br />
      5. Retention of personal data
      <br />
      <br />
      Trendteller will retain your personal information only for as long as is
      necessary for the purposes set out in this Data Protection Policy.
      <br />
      <br />
      Trendteller will retain and use your information to the extent necessary
      to comply with our legal obligations, resolve disputes, and enforce our
      policies.
      <br />
      <br />
      6. Data protection rights
      <br />
      <br />
      If you are a resident of the European Economic Area (EEA), you have
      certain data protection rights. If you wish to be informed what personal
      data we hold about you and if you want it to be removed from our systems,
      please contact us.
      <br />
      <br />
      In certain circumstances, you have the following data protection rights:
      <br />
      <br />
      ● The right to access, update or to delete the information we have on you
      <br />
      <br />
      ● The right of rectification
      <br />
      <br />
      ● The right to object
      <br />
      <br />
      ● The right of restriction
      <br />
      <br />
      ● The right to data portability
      <br />
      <br />
      ● The right to withdraw consent
      <br />
      <br />
    </span>
  );

  return (
    <>
      <div id="tutorial-pg">
        <SummaryTextView
          hasLoaded={true}
          title={"Terms and Conditions"}
          text={terms}
        />
        <SummaryTextView
          hasLoaded={true}
          title={"Privacy Policy"}
          text={privacy}
        />
      </div>
    </>
  );
}

export default Legal;
