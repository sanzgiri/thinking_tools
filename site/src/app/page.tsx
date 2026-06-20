import { getTools } from '@/lib/tools';
import ToolBrowser from './ToolBrowser';
import styles from './page.module.css';

export default function Home() {
  const tools = getTools();

  return (
    <div className={styles.container}>
      <header className={styles.header}>
        <h1 className={styles.title}>Dennett&apos;s Thinking Tools</h1>
        <p className={styles.subtitle}>
          A comprehensive collection of 77 intuition pumps and tools for thinking from Daniel Dennett.
        </p>
      </header>

      <ToolBrowser tools={tools} />

      <footer className={styles.footer}>
        <p>Based on &quot;Intuition Pumps and Other Tools for Thinking&quot; by Daniel C. Dennett.</p>
      </footer>
    </div>
  );
}
