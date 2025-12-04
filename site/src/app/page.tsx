import Link from 'next/link';
import { getTools } from '@/lib/tools';
import styles from './page.module.css';

export default function Home() {
  const tools = getTools();
  const categories = Array.from(new Set(tools.map(t => t.category)));
  const sortedTools = [...tools].sort((a, b) => a.name.localeCompare(b.name));

  return (
    <div className={styles.container}>
      <header className={styles.header}>
        <h1 className={styles.title}>Dennett's Thinking Tools</h1>
        <p className={styles.subtitle}>
          A comprehensive collection of 77 intuition pumps and tools for thinking from Daniel Dennett.
        </p>
      </header>

      <nav style={{
        maxWidth: '80rem',
        margin: '0 auto 4rem',
        padding: '1.5rem',
        backgroundColor: 'var(--card-bg)',
        borderRadius: '0.75rem',
        border: '1px solid var(--card-border)'
      }}>
        <h3 style={{ fontSize: '1.25rem', marginBottom: '1rem', color: 'var(--text-color)' }}>Browse by Category</h3>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.75rem' }}>
          {categories.map(cat => (
            <a key={cat} href={`#${cat}`} style={{
              padding: '0.5rem 1rem',
              backgroundColor: 'rgba(34, 211, 238, 0.1)',
              color: 'var(--primary-color)',
              borderRadius: '9999px',
              fontSize: '0.875rem',
              fontWeight: 600,
              textDecoration: 'none',
              transition: 'background-color 0.2s'
            }}>
              {cat}
            </a>
          ))}
          <a href="#alphabetical" style={{
            padding: '0.5rem 1rem',
            backgroundColor: 'rgba(168, 85, 247, 0.1)',
            color: 'var(--secondary-color)',
            borderRadius: '9999px',
            fontSize: '0.875rem',
            fontWeight: 600,
            textDecoration: 'none'
          }}>
            Alphabetical Index
          </a>
        </div>
      </nav>

      <main className={styles.main}>
        {categories.map(category => (
          <section key={category} id={category} className={styles.categorySection}>
            <h2 className={styles.categoryTitle}>{category}</h2>
            <div className={styles.grid}>
              {tools.filter(t => t.category === category).map(tool => (
                <Link href={`/tool/${tool.slug}`} key={tool.number} className={styles.cardLink}>
                  <div className={styles.card}>
                    <div className={styles.cardHeader}>
                      <span className={styles.toolNumber}>#{tool.number}</span>
                      <span className={styles.toolCategory}>{tool.category}</span>
                    </div>
                    <h3 className={styles.toolName}>{tool.name}</h3>
                    <p className={styles.toolDesc}>{tool.short_description}</p>
                  </div>
                </Link>
              ))}
            </div>
          </section>
        ))}

        <section id="alphabetical" className={styles.categorySection} style={{ marginTop: '6rem', paddingTop: '2rem', borderTop: '1px solid var(--card-border)' }}>
          <h2 className={styles.categoryTitle} style={{ color: 'var(--secondary-color)' }}>Alphabetical Index</h2>
          <div style={{ columnCount: 2, columnGap: '2rem' }}>
            {sortedTools.map(tool => (
              <div key={tool.number} style={{ marginBottom: '0.5rem', breakInside: 'avoid' }}>
                <Link href={`/tool/${tool.slug}`} style={{
                  color: 'var(--text-muted)',
                  textDecoration: 'none',
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'baseline',
                  padding: '0.25rem 0'
                }}>
                  <span style={{ color: 'var(--text-color)', fontWeight: 500 }}>{tool.name}</span>
                  <span style={{ fontSize: '0.75rem', opacity: 0.5 }}>#{tool.number}</span>
                </Link>
              </div>
            ))}
          </div>
        </section>
      </main>

      <footer className={styles.footer}>
        <p>Based on "Intuition Pumps and Other Tools for Thinking" by Daniel C. Dennett.</p>
      </footer>
    </div>
  );
}
