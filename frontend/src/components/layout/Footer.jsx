import React from "react";

export function Footer() {
  return (
    <div className="footerbar">
      <div className="container">
        <div className="footergrid">
          <div>
            <p className="ftitle">STAY IN TOUCH</p>
            <div className="fmuted">
              VK • Facebook • Twitter • Instagram
              <br />
              <br />
              Subscribe to get news and offers.
            </div>
          </div>

          <div>
            <p className="ftitle">LET'S CONNECT</p>
            <input className="finput" placeholder="Email address*" />
            <button className="fbtn">OK</button>
          </div>

          <div>
            <p className="ftitle">NEED HELP?</p>
            <div className="fmuted">
              +7 (123) 456-78-90
              <br />
              info@mewo.com
            </div>
          </div>
        </div>

        <div className="copy">© 2026 Clothing Store "SWAGSTORE".</div>
      </div>
    </div>
  );
}
