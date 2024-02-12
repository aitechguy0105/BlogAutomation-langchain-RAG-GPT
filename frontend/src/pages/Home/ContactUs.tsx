import axios from "axios";
import { Form, Input, message } from "antd";
import { basic_url } from "@/stack/stack";
import TextArea from "antd/es/input/TextArea";

const validateMessages = {
    required: '${label} is required!',
    types: {
        email: '${label} is not a valid email!',
    },
    number: {
        range: '${label} must be between ${min} and ${max}',
    },
};


const ContactUs = () => {

    const handleSendBtn = () => {
        console.log('ClickSendButton')
    }

    const onFinish = (value: any) => {
        console.log(value.user, value.email, value.message);
        
        axios.post(`${basic_url}contact_us/${value.user}/${value.email}/${value.message}`,).then(() => {
            message.success("Left Message Successfully.")
        }).catch(() => message.error("Newtwork Error") )
    };

    return (
        <>
            <div className="container mt-[150px] flex lg:flex-row flex-col  lg:gap-10 gap-24">
                <div className="basis-[35%] flex flex-col gap-10">
                    <div className="bg-[#1d4354] text-[white] text-5xl py-5 pl-5 pr-10 ">
                        Contact Info
                    </div>
                    <div className="flex items-center gap-5">
                        <i className="fa fa-building" style={{ fontSize:"30px"}}></i>
                        <p style={{fontFamily: "cursive"}}>VV, LLC Company</p>
                    </div>
                    <div className="flex items-center gap-5">
                        <i className="fas fa fa-map-marker" style={{ fontSize: "40px" }}></i>
                        <p style={{fontFamily: "cursive"}}>90 Richmond Hill road, 1M S.I, New York 10314</p>
                    </div>
                    <div className="flex items-center gap-5">
                        <i className="fas fa fa-phone" style={{ fontSize: "33px" }}></i>
                        <p style={{fontFamily: "cursive"}}>732-701-7571</p>
                    </div>
                    <div className="flex items-center gap-5">
                        <i className="fas fa fa-envelope" style={{ fontSize: "30px" }}></i>
                        <p style={{fontFamily: "cursive"}}>goldexcg@outlook.com</p>
                    </div>
                </div>
                <div className="basis-[65%] flex flex-col gap-10 mb-14">
                    <div className="bg-[#1d4354] text-[white] text-5xl py-5 pl-5 pr-10">
                        Leave Us Message
                    </div>

                    <Form
                        name="nest-messages"
                        layout="vertical"
                        labelWrap
                        colon={false}
                        onFinish={onFinish}
                        style={{ maxWidth: 1000 }}
                        validateMessages={validateMessages}
                    >
                        <div className="flex w-full justify-between">
                            <Form.Item name={['user']} label={
                                <p style={{ fontSize: '20px' }}>Your Name</p>
                            }
                                rules={[{ required: true }]}
                                style={{width:'40%'}}
                            >
                                <Input size="large"/>
                            </Form.Item>
                            <Form.Item name={['email']} label={
                                <p style={{ fontSize: '20px' }}>Your Email Address</p>
                            }
                                rules={[{ type: 'email', required: true }]}
                                style={{width:'40%'}}
                            >
                                <Input size="large" />
                            </Form.Item>
                        </div>
                        <Form.Item name={['message']} style={{width:'100%'}} label={
                            <p style={{ fontSize: '20px' }}>Message</p>
                        }
                            rules={[{required:true}]}
                        >
                            <TextArea style={{height:150}}></TextArea>
                        </Form.Item>
                        <Form.Item>
                            <button type="submit" className=" w-full border rounded-[5px] px-10 py-3 font-sans font-bold text-base text-[white] bg-[#1d4354]" onClick={handleSendBtn}>Send</button>
                        </Form.Item>
                    </Form>
                </div>
            </div>
        </>
    )
}

export default ContactUs;