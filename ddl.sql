CREATE TABLE lj_house( 
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT COMMENT '主键',
    house_id BIGINT COMMENT '备案编号',
    house_url_id BIGINT COMMENT '链家编号',
    total_price int COMMENT '总价',
    unit_price int COMMENT '单价',
    total_square int COMMENT '总面积',
    area VARCHAR(50) COMMENT '所在区',
    street VARCHAR(20) COMMENT '所在街道',
    city VARCHAR(20) COMMENT '所在城市',
    community VARCHAR(100) COMMENT '小区名称',
    build_time VARCHAR(50) COMMENT '建造年代',
    house_style VARCHAR(50) COMMENT '户型',
    floor VARCHAR(20) COMMENT '楼层',
    sale_date DATETIME COMMENT '挂牌时间',
    decoration VARCHAR(50) COMMENT '装修情况',
    hold_time VARCHAR(50) COMMENT '房屋年限（是否满五）',
    price_update_times int DEFAULT 0 COMMENT '调价次数',
    price_diff int DEFAULT 0 COMMENT '调价差值',
    link VARCHAR(200) COMMENT '链接',
    created_date DATETIME COMMENT '创建时间',
    modified_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间')ENGINE = InnoDB COMMENT 'lj' DEFAULT CHARSET=utf8;





-- https://hz.lianjia.com/ershoufang/103101670128.html
