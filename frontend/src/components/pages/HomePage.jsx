import React from "react";
import { Link } from "react-router-dom";

export function HomePage() {
    return (
        <>
            <div className="hero">
                <div className="hero-inner">
                    <div className="hero-card">
                        <div className="hero-title">AUTUMN & WINTER</div>
                        <Link className="hero-btn" to="/shop">
                            SHOP NOW
                        </Link>
                    </div>
                </div>
            </div>

            <div className="section">
                <div className="container">
                    <h2 className="h1">ALL YEAR ROUND</h2>
                    <div className="divider" />
                    <p className="sub" style={{ marginTop: 18 }}>
                        Essentials for your wardrobe
                    </p>

                    <div className="feature-grid">
                        <Link to="/shop" className="tile">
                            <div
                                className="tile-img"
                                style={{
                                    backgroundImage:
                                        'url("https://static.wixstatic.com/media/cda177_f95b14c95d6446de847782f0b6fd0027.png/v1/fill/w_596,h_708,al_c,q_90,usm_0.66_1.00_0.01/cda177_f95b14c95d6446de847782f0b6fd0027.webp")',
                                }}
                            />
                            <div className="tile-label">MIDI SKIRT</div>
                        </Link>

                        <Link to="/sale" className="tile tile-sale">
                            <div className="tile-mid">
                                <div>
                                    <h3>SALE</h3>
                                    <p>Best offers</p>
                                </div>
                            </div>
                            <div
                                className="tile-img"
                                style={{
                                    backgroundImage:
                                        'url("https://static.wixstatic.com/media/cda177_b5a795ade21b41d38cadd836824e6768.jpg/v1/fill/w_298,h_410,al_c,q_80,usm_0.66_1.00_0.01,enc_avif,quality_auto/cda177_b5a795ade21b41d38cadd836824e6768.jpg 1x, https://static.wixstatic.com/media/cda177_b5a795ade21b41d38cadd836824e6768.jpg/v1/fill/w_526,h_724,al_c,q_85,enc_avif,quality_auto/cda177_b5a795ade21b41d38cadd836824e6768.jpg 2x")',
                                }}
                            />
                        </Link>
                        <Link to="/shop" className="tile">
                            <div
                                className="tile-img"
                                style={{
                                    backgroundImage:
                                        'url("https://static.wixstatic.com/media/84770f_9a81715dcb4b43fa936d243fcd90e2a9.png/v1/fill/w_596,h_708,al_c,q_90,usm_0.66_1.00_0.01/84770f_9a81715dcb4b43fa936d243fcd90e2a9.webp")',
                                }}
                            />
                            <div className="tile-label">VINTAGE SUNGLASSES</div>
                        </Link>
                    </div>
                </div>
            </div>
        </>
    );
}
