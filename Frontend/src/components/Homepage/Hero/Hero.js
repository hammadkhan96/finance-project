import React from 'react'
import { useState } from 'react'
import Button from 'react-bootstrap/Button';
import { Container, Row, Col } from 'react-bootstrap';
import lifeIns from "../../../assets/images/life.jpg"
import Image from 'next/image'
import axios from "axios";
import { toast } from 'react-toastify';
const Hero = () => {

    const [formdata, setFormData] = useState(false)

    const handleSubmit = () => {
        setFormData(true)
    }

    const [userData, setUserData] = useState({
        purpose: "",
        amount: "",
        duration: ""

    });

    const [errorPurpose, setErrorPurpose] = useState("");
    const [errorAmmount, setErrorAmmount] = useState("");
    const [errorDuration, setErrorDuration] = useState("");


    const handleSubmitData = async () => {
    
        if (userData?.amount === ""  ||  userData?.amount === "null") {
            setErrorAmmount("Please Enter Your Ammount");
            return
        }

        if (userData?.purpose === ""  ||  userData?.purpose === "null") {
            setErrorPurpose("Please Select Your Purpose");
            return
        }

        if (userData?.duration === ""  ||  userData?.duration === "null") {
            setErrorDuration("Please Enter Your Duration");
            return
        }
    
        axios.post(`http://127.0.0.1:8000/api/request/create`, userData)
        .then(function (response) {
          if(response.status == 200){
            console.log('SUBMIT...')
            setFormData(false)
            setUserData({
                purpose: "",
                amount: "",
                duration: ""
            })
            toast.success("Request Successfully Submitted");
          }
          console.log('SUBMIT DATA...', response)
        })
        .catch(function (error) {
          console.log(error)
        });
    }
    

   
  return (
      <div className='hero__page_1'>
        <div className='hero__heading'>
            <h2 id='hero__heading'>INVESTOR ANGEL</h2>
        </div>
            <img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhhtiwNp_GGXVBTIBHgwcU1iQfvBwGcNpEWws17jURxLgsTocyKGMzAWZK5-mNe3XprsjDz36yis19PmnSKvpEtg_Lbwto3pgFoOSTxCqcwp_v5OsNqRl23bzqssv8epDnNQazhL2AB1OuITxdhlqfv_YsXirU0W_mbfLYisiFPYgR1G0cpo9RumyNMq5M/s1600/cloud-03.png" alt="" className="cloud1" />
            <img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjgpQUDtHjzt5ERnQ41HOOChn4ruWGjmY72CqEtryfk_IOvHn9rrcf_JNlvREpx0tLcc2vPbThJfuKRcDDE1sVBVism3kDKSL3EqPoPqy3z09gCfjcw3UzCpoeGCHj5O397FDzu-4tVI7R36f-zd73bFw_C3k4N_2bR5wRl-D-Ae1_wJZMMe2aPp3qmWLk/s1600/cloud-01.png" alt="" className="cloud2" />
            <img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgtF2ldV1Z-0zEQa0NUSzO7bLUVRXyaAXBiWGcXQrl4dQC2fCoMHaxSblPg57hTZlR5j16VEVpvmAA0k_hmo45uSdDu5q1bL7jQOaJqFJjeb_B62tgepM6Rig8uQNey1WojLy4zvbUKmPlDbcL_hzhHiX0nhIwJEefJ1XLfRNi1_yuMI08XzDPVOa_ds0U/s1600/cloud-04.png" alt="" className="cloud3" />
            <img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhhtiwNp_GGXVBTIBHgwcU1iQfvBwGcNpEWws17jURxLgsTocyKGMzAWZK5-mNe3XprsjDz36yis19PmnSKvpEtg_Lbwto3pgFoOSTxCqcwp_v5OsNqRl23bzqssv8epDnNQazhL2AB1OuITxdhlqfv_YsXirU0W_mbfLYisiFPYgR1G0cpo9RumyNMq5M/s1600/cloud-03.png" alt="" className="cloud4" />
            <img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgtF2ldV1Z-0zEQa0NUSzO7bLUVRXyaAXBiWGcXQrl4dQC2fCoMHaxSblPg57hTZlR5j16VEVpvmAA0k_hmo45uSdDu5q1bL7jQOaJqFJjeb_B62tgepM6Rig8uQNey1WojLy4zvbUKmPlDbcL_hzhHiX0nhIwJEefJ1XLfRNi1_yuMI08XzDPVOa_ds0U/s1600/cloud-04.png" alt="" className="cloud5" />
       
       {formdata ? <>
        <div className='hero_formData'>
            <button onClick={()=> setFormData(false)} className='onClose'>
                <svg viewPort="0 0 12 12" version="1.1"
                    xmlns="http://www.w3.org/2000/svg">
                    <line x1="1" y1="11" 
                        x2="11" y2="1" 
                        stroke="black" 
                        stroke-width="2"/>
                    <line x1="1" y1="1" 
                        x2="11" y2="11" 
                        stroke="black" 
                        stroke-width="2"/>
                </svg>
            </button>
            <form>
                <div className='formGroup'>
                    <label>Q1. How much do you want to invest in USD?</label>
                    <input type='text'
                    value={userData?.amount}
                    onChange={({ target }) => { setUserData((prev) => ({ ...prev, amount: target?.value })); setErrorAmmount("")}}
                    />
                </div>
                <p className="register_form_error">{errorAmmount}</p>

                <div className='formGroup'>
                    <label>Q2. For what purpose?</label>
                    <select
                    value={userData?.purpose}
                    onChange={({ target }) => { setUserData((prev) => ({ ...prev, purpose: target?.value })); setErrorPurpose("")}}
                    >
                        <option value="">Select Option</option>
                        <option value="Retirement Planning">Retirement Planning</option>
                        <option value="Purchasing a Home">Purchasing a Home</option>
                        <option value="Education Planning">Education Planning</option>
                        <option value="Looking to Get Started">Looking to Get Started</option>
                        <option value="Looking to Speculate">Looking to Speculate</option>
                    </select>
                </div>
                <p className="register_form_error">{errorPurpose}</p>

                <div className='formGroup'>
                    <label>Q3. For how long do you plan to invest?</label>
                    <input type='text'
                    value={userData?.duration}
                    onChange={({ target }) => { setUserData((prev) => ({ ...prev, duration: target?.value })); setErrorDuration("")}}
                    />
                </div>
                <p className="register_form_error">{errorDuration}</p>

                <div className='formGroup'>
                    <a href="javascript:void(0)" className='submit_btn'
                    onClick={() => {
                        // setAppliedFormBtn(handleSubmit)
                        handleSubmitData(userData)
                      }}
                    >Submit</a>
                </div>
            </form>
        </div>
       </> : <>
        <div className='hero__page_2__sub_heading'>
            <h3>Building wealth takes time</h3>
            <h4>Let’s get you started</h4>
        </div>

        <div className='hero_buttons'>
            <button>Watch the introductory video</button>
            <button onClick={handleSubmit}>Jump right into the questions</button>
        </div>
        </>} 
      </div>
  )
}

export default Hero
