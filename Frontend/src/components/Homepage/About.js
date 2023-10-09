import React from 'react'
import { Container, Row, Col } from 'react-bootstrap';
import aboutUs from "../../assets/images/about_us.jpg"
import Image from 'next/image'

const About = () => {
  return (
    <div className='hero__page_2'>
    <Container>
        <Row>
            <Col md={12}>
                <h2 className='heading_default'>About Us</h2>
            </Col>
        </Row>

        <Row className='mt-5 mb-5'>
            <Col md={6}>
                <div className='about_us__content'>
                    <p>It’s not about us.  It’s about YOU.  We’re not asking you to open an account with us.  We’re not asking for personal information such as your Social Security number.  And we’re definitely not asking for your phone number so that we can call you on a Sunday morning – yes, at least one financial website has done exactly that! (But we are asking for your email so that we can keep in touch with you.) </p>
                    <p>This site is for you:  to provide you with financial resources and tools with which you grow your wealth.  By ‘you,’ we are referring to the novice investor, the teenager who has no money yet but wants to learn, the newly married couple who just paid off their student loans and want to get started in the markets, or the newly-retired go-getter who wants to take a “DIY” approach.</p>
                    <p>Investing has become an over-complicated affair – the Wall Street crowd loves it that way and profits accordingly.  But we aim to distill all the investment noise to its most core essentials, yet still provide you with the necessary tools to make a wise decision. How do we know how to do this? </p>
                    <p>The founder of this site holds the CFA designation and is also a Certified Financial Planner who has spent over 20 years in finance working for a big Wall Street firm as well as two of the ubiquitous “too big to fail” banks that dominate the American financial landscape. </p>
                    <p>As such, a long and growing career of understanding basic principles are laid out in this site; we hope, for your benefit and learning. The co-creator of this site is a machine-learning specialist who personally built out the Monte Carlo models herein that are so pivotal in helping you envision the power of compounded investing. </p>
                    <p>We combined our talents with one goal in mind:  to help you build your wealth. We hope this website is as fun for you to work through as it was for us to build it. </p>
                    <p className='gold_color__p'>Happy investing everyone! Thank you for visiting our site.</p>
                </div>
            </Col>
            <Col>
                <div>
                    {/* <img src={aboutUs} /> */}
                    <Image
                    src={aboutUs}
                    height={790}
                    alt="Picture of the author"
                    />
                </div>
            </Col>
        </Row>
    </Container>
  </div>
  )
}

export default About
