import { useRef, useEffect } from "react";
import axios from "axios";
import { Modal, Form, Input, message } from "antd";
import emailjs from "@emailjs/browser";
import { InputRef } from "antd/es/input";
import { setAuthToken } from "@/Middlewares/setAuthTokens";
import "./Header.css";
import { basic_url } from "@/stack/stack";


const validateMessages = {
    required: '${label} is required!',
    types: {
        email: '${label} is not a valid email!',
    },
};


type props = {
    visible: number,
    setVisible: any,
}


const LoginModal = ({ visible, setVisible }: props) => {

    const nameRef = useRef<InputRef>(null);
    const emailRef = useRef<InputRef>(null);
    // const [loading, setLoading] = useState(false);

    useEffect(() => {
        emailjs.init("5NpiwcY84jr3V0wmR");
    }, []);

    const handleCancelSignup = () => {
        setVisible(0);
    };

    const handleClickSignup = async(values: any) => {
        const serviceId = "service_ud6o1lf";
        const templateId = "template_hktbi39";
        if(emailRef.current && nameRef.current) {
            try {
                // setLoading(true);
                await emailjs.send(serviceId, templateId, {
                  name:nameRef.current.input?.value,
                  recipient: emailRef.current.input?.value
                });
                alert("email successfully sent check inbox");
              } catch (error) {
                message.error("Error");
              } finally {
                // setLoading(false);
              }
        }
        await axios.post(`${basic_url}users/`, values).then((res) => {
            if(res.data.jwt_token){
                message.success("Successfully Signed up.")
            }
            else message.warning(res.data.error)
        })
        .catch(() => {message.error("Error Network")})
    }

    const signupToLogin = () => {
        setVisible(2)
    }

    const loginToSignup = () => {
        setVisible(1);
    }

    const handleClickLogin = (values: any) => {
        axios.post(`${basic_url}users/login`, values).then((res) => {
            console.log(res.data);
            if(res.data.jwt_token){
                message.success("Successfully Logined.")
                const token = res.data.jwt_token;
                localStorage.setItem("token", token);
                setAuthToken(token);
                window.location.href = '/'
            }
            else message.warning(res.data.error)
        })
        .catch(() => {message.error("Error Network")})
    }

    const onFinishFailed = (errorInfo: any) => {
        console.log('Failed:', errorInfo);
    };

    return (
        <>
            <Modal open={visible === 1 && true} width={500} onCancel={handleCancelSignup} className="signup-modal" footer={null}>
                <div className="w-full h-[450px] flex flex-col">
                    <div className="font-bold text-2xl text-[#053243] mt-5 ml-3">
                        <span className="text-[#a48527]">GOLD</span> EXCHANGE
                    </div>
                    <div className="font-bold text-5xl text-[#053243] mx-auto mt-5">
                        Sign Up
                    </div>
                    <div className="mt-10">
                        <Form
                            name="basic"
                            labelCol={{ span: 8 }}
                            wrapperCol={{ span: 16 }}
                            style={{ maxWidth: 400 }}
                            onFinish={handleClickSignup}
                            onFinishFailed={onFinishFailed}
                            autoComplete="off"
                            validateMessages={validateMessages}
                        >
                            <Form.Item
                                label="Full Name"
                                name="name"
                                rules={[{ required: true }]}
                            >
                                <Input/>
                            </Form.Item>
                            <Form.Item
                                label="Email"
                                name="email"
                                rules={[{ type: "email", required: true }]}
                            >
                                <Input ref={emailRef}/>
                            </Form.Item>

                            <Form.Item
                                label="Password"
                                name="password"
                                rules={[{ required: true }]}
                            >
                                <Input.Password />
                            </Form.Item>

                            <Form.Item wrapperCol={{ offset: 8, span: 16 }}>
                                <button type="submit" className="w-[190px] rounded-[4px] h-[40px] bg-[#053243] text-[white] text-xl font-mono mt-5">
                                    SignUp
                                </button>
                            </Form.Item>
                        </Form>
                    </div>
                    <div className="mx-auto text-[#053243] text-[18px]">
                        If you have already signed up, click <button className=" underline" onClick={signupToLogin}>here</button> to log in.
                    </div>
                </div>
            </Modal>
            <Modal open={visible === 2 && true} width={500} onCancel={handleCancelSignup} className="signup-modal" footer={null}>
                <div className="w-full h-[450px] flex flex-col">
                    <div className="font-bold text-2xl text-[#053243] mt-5 ml-3">
                        <span className="text-[#a48527]">GOLD</span> EXCHANGE
                    </div>
                    <div className="font-bold text-5xl text-[#053243] mx-auto mt-5">
                        Log in
                    </div>
                    <div className="mt-10">
                        <Form
                            name="basic1"
                            labelCol={{ span: 8 }}
                            wrapperCol={{ span: 16 }}
                            style={{ maxWidth: 400 }}
                            onFinish={handleClickLogin}
                            onFinishFailed={onFinishFailed}
                            autoComplete="off"
                            validateMessages={validateMessages}
                        >
                            <Form.Item
                                label="Email"
                                name="email"
                                rules={[{ type: "email", required: true }]}
                            >
                                <Input />
                            </Form.Item>

                            <Form.Item
                                label="Password"
                                name="password"
                                rules={[{ required: true }]}
                            >
                                <Input.Password />
                            </Form.Item>

                            <Form.Item wrapperCol={{ offset: 8, span: 16 }}>
                                <button type="submit" className="w-[190px] rounded-[4px] h-[40px] bg-[#053243] text-[white] text-xl font-mono mt-5">
                                    Login
                                </button>
                            </Form.Item>
                        </Form>
                    </div>
                    <div className="mx-auto text-[#053243] text-[18px]">
                        If you have not already signed up, click <button className=" underline" onClick={loginToSignup}>here</button> to sign up.
                    </div>
                </div>
            </Modal>

        </>
    )
}

export default LoginModal;