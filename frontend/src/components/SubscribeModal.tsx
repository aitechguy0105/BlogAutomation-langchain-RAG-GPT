import axios from "axios";
import { Modal, Form, Input, message } from "antd";
import { basic_url } from "@/stack/stack";


type props = {
    visible: boolean,
    setVisible: any,
}

// const layout = {
//     labelCol: { span: 16 },
//     wrapperCol: { span: 16 },
// };

const validateMessages = {
    required: '${label} is required!',
    types: {
        email: '${label} is not a valid email!',
    },
    number: {
        range: '${label} must be between ${min} and ${max}',
    },
};

const SubscribeModal = ({ visible, setVisible }: props) => {


    const handleOk = () => {
        setVisible(false);
    };

    const handleCancel = () => {
        setVisible(false);
    };

    const onFinish = (value: any) => {
        setVisible(false);
        if(value.email !== undefined){
            axios.post(`${basic_url}subscribers/subscribe_email/${value.email}`).then(() => {
                message.success("Subscribed your email successfully.")
            }).catch((err) => {
                message.error(err.response.data.error)
            })
        }
      };

    return (
        <>
            <Modal open={visible} width={650} onOk={handleOk} onCancel={handleCancel} title="Subscribe" className="custom-modal" footer={null}>
                <Form
                    // {...layout}
                    // layout="vertical"
                    name="nest-messages"
                    // labelAlign="vertical"
                    layout="vertical"
                    labelWrap
                    colon={false}
                    onFinish={onFinish}
                    style={{ maxWidth: 600 }}
                    validateMessages={validateMessages}
                >
                    <Form.Item name={['email']} label={
                            <p style={{fontSize:'20px'}}>Your Email Address</p>
                        }
                        rules={[{ type: 'email', required:true }]}
                        
                        >
                        <Input size="large"/>
                    </Form.Item>
                    <Form.Item >
                        <button type="submit" className=" w-full border rounded-[5px] px-10 py-3 font-sans font-bold text-base text-[white] bg-[#1d4354]" onClick={onFinish}>Sign up</button>
                    </Form.Item>
                </Form>
            </Modal>
        </>
    )
}

export default SubscribeModal;