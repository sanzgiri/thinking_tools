import { getTools, getToolBySlug, getToolContent } from '@/lib/tools';
import ReactMarkdown from 'react-markdown';
import Link from 'next/link';
import styles from './page.module.css';
import { notFound } from 'next/navigation';

export async function generateStaticParams() {
    const tools = getTools();
    return tools.map((tool) => ({
        slug: tool.slug,
    }));
}

export default async function ToolPage({ params }: { params: Promise<{ slug: string }> }) {
    const { slug } = await params;
    const tool = getToolBySlug(slug);
    const content = getToolContent(slug);

    if (!tool) {
        notFound();
    }

    return (
        <div className={styles.container}>
            <Link href="/" className={styles.backLink}>
                ← Back to Index
            </Link>

            <header className={styles.header}>
                <div className={styles.meta}>
                    <span className={styles.number}>Tool #{tool.number}</span>
                    <span className={styles.category}>{tool.category}</span>
                </div>
                <h1 className={styles.title}>{tool.name}</h1>
                <p className={styles.shortDesc}>{tool.short_description}</p>
            </header>

            <article className={styles.content}>
                {content ? (
                    <ReactMarkdown>{content}</ReactMarkdown>
                ) : (
                    <div style={{
                        padding: '2rem',
                        textAlign: 'center',
                        border: '1px dashed #334155',
                        borderRadius: '0.75rem',
                        backgroundColor: 'rgba(30, 41, 59, 0.5)'
                    }}>
                        <h3 style={{ fontSize: '1.25rem', fontWeight: 'bold', color: '#cbd5e1', marginBottom: '0.5rem' }}>
                            Content Generating...
                        </h3>
                        <p style={{ color: '#64748b', marginBottom: '1.5rem' }}>
                            The detailed guide for this tool is currently being generated.
                            Please check back soon.
                        </p>
                        <div style={{
                            textAlign: 'left',
                            maxWidth: '30rem',
                            margin: '0 auto',
                            backgroundColor: '#020617',
                            padding: '1rem',
                            borderRadius: '0.5rem',
                            border: '1px solid #1e293b'
                        }}>
                            <h4 style={{ fontSize: '0.875rem', fontWeight: 'bold', color: '#94a3b8', marginBottom: '0.5rem' }}>
                                Base Description:
                            </h4>
                            <p style={{ fontSize: '0.875rem', color: '#e2e8f0' }}>
                                {tool.detailed_description}
                            </p>
                        </div>
                    </div>
                )}
            </article>

            <div className={styles.footer}>
                <Link href="/" className={styles.backButton}>
                    Back to All Tools
                </Link>
            </div>
        </div>
    );
}
