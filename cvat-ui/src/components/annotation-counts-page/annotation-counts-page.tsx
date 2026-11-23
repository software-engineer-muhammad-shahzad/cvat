// Copyright (C) CVAT.ai Corporation
//
// SPDX-License-Identifier: MIT

import 'chart.js/auto';
import React, { useCallback, useEffect, useState } from 'react';
import { useParams } from 'react-router';
import { Link } from 'react-router-dom';
import { Bar } from 'react-chartjs-2';
import { Row, Col } from 'antd/lib/grid';
import Button from 'antd/lib/button';
import Empty from 'antd/lib/empty';
import Result from 'antd/lib/result';
import Spin from 'antd/lib/spin';
import Title from 'antd/lib/typography/Title';
import Text from 'antd/lib/typography/Text';

import { getCore } from 'cvat-core-wrapper';

const core = getCore();

interface LabelCount {
    label: string;
    count: number;
}

interface AnnotationCounts {
    task_id: number;
    total: number;
    counts: LabelCount[];
}

type PageState =
    | { status: 'loading' }
    | { status: 'error'; message: string }
    | { status: 'ready'; data: AnnotationCounts };

const BAR_HEIGHT_PX = 22;
const MIN_CHART_HEIGHT_PX = 300;

function AnnotationCountsPage(): JSX.Element {
    const taskId = +useParams<{ tid: string }>().tid;
    const [state, setState] = useState<PageState>({ status: 'loading' });

    const loadCounts = useCallback(async (): Promise<void> => {
        setState({ status: 'loading' });
        try {
            const response = await core.server.request(
                `/api/test/tasks/${taskId}/annotation-counts`,
                { method: 'GET' },
            );
            setState({ status: 'ready', data: response.data });
        } catch (error: unknown) {
            const message = error instanceof Error ? error.message : String(error);
            setState({ status: 'error', message });
        }
    }, [taskId]);

    useEffect(() => {
        loadCounts();
    }, [loadCounts]);

    let content: JSX.Element;
    if (state.status === 'loading') {
        content = <Spin size='large' />;
    } else if (state.status === 'error') {
        content = (
            <Result
                status='error'
                title='Could not load annotation counts'
                subTitle={state.message}
                extra={<Button type='primary' onClick={loadCounts}>Retry</Button>}
            />
        );
    } else if (state.data.total === 0) {
        content = <Empty description='This task has no annotations yet' />;
    } else {
        const { counts, total } = state.data;
        content = (
            <>
                <Text>{`${total} annotations across ${counts.length} labels`}</Text>
                <div style={{ height: Math.max(MIN_CHART_HEIGHT_PX, counts.length * BAR_HEIGHT_PX) }}>
                    <Bar
                        data={{
                            labels: counts.map((item) => item.label),
                            datasets: [{
                                label: 'Annotations',
                                data: counts.map((item) => item.count),
                                backgroundColor: '#1890ff',
                            }],
                        }}
                        options={{
                            indexAxis: 'y',
                            maintainAspectRatio: false,
                            plugins: { legend: { display: false } },
                        }}
                    />
                </div>
            </>
        );
    }

    return (
        <Row justify='center' style={{ padding: 24 }}>
            <Col span={20}>
                <Link to={`/tasks/${taskId}`}>Back to task</Link>
                <Title level={4}>{`Annotation counts for task #${taskId}`}</Title>
                {content}
            </Col>
        </Row>
    );
}

export default AnnotationCountsPage;