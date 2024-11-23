import {LoadingOutlined} from '@ant-design/icons';
import {Flex, Spin} from 'antd';

import React from 'react';

const Loader = () => {
    return (
        <Flex align="center" gap="middle">
            <Spin indicator={<LoadingOutlined style={{fontSize: 48}} spin/>}/>
        </Flex>
    );
};

export default Loader;
