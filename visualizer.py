import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

class PJMAVisualizer:
    def __init__(self, file_path='data/jobs_clean.csv'):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Cleaned data not found at {file_path}")
        self.df = pd.read_csv(file_path)
        os.makedirs('outputs/visuals', exist_ok=True)

    def plot_skill_dominance(self, tech_only=True):
        """Generates a frequency distribution of top skills."""
        data = self.df[self.df['is_tech'] == 1] if tech_only else self.df
        
        # Explode skills into individual rows for counting
        skills_series = data['skills'].str.split(',').explode().str.strip()
        top_skills = skills_series[skills_series != 'not specified'].value_counts().head(15).reset_index()
        top_skills.columns = ['Skill', 'Count']

        fig = px.bar(
            top_skills, x='Count', y='Skill', orientation='h',
            title='Top 15 Technical Skills in Demand (Pakistan 2026)',
            color='Count', color_continuous_scale='Viridis',
            template='plotly_dark'
        )
        fig.write_html("outputs/visuals/skill_dominance.html")
        return fig

    def plot_city_distribution(self):
        """Visualizes the geographic concentration of job openings."""
        city_counts = self.df['location'].value_counts().reset_index()
        city_counts.columns = ['City', 'Jobs']

        fig = px.pie(
            city_counts, values='Jobs', names='City',
            title='Market Share by Metropolitan Hub',
            hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel,
            template='plotly_dark'
        )
        fig.update_traces(textinfo='percent+label')
        fig.write_html("outputs/visuals/city_distribution.html")
        return fig

    def plot_experience_heatmap(self):
        """Correlates required experience with tech-role density."""
        fig = px.box(
            self.df, x='location', y='exp_years', color='is_tech',
            title='Experience Requirements by City and Role Type',
            labels={'exp_years': 'Years of Experience', 'is_tech': 'Tech Role'},
            notched=True, template='plotly_dark'
        )
        fig.write_html("outputs/visuals/experience_heatmap.html")
        return fig

    def plot_remote_index(self):
        """Quantifies the prevalence of remote-capable roles."""
        remote_data = self.df['is_remote'].map({1: 'Remote', 0: 'On-site'}).value_counts().reset_index()
        remote_data.columns = ['Work Type', 'Count']

        fig = px.treemap(
            remote_data, path=['Work Type'], values='Count',
            title='Remote vs. On-site Work Distribution',
            color='Count', color_continuous_scale='RdBu',
            template='plotly_dark'
        )
        fig.write_html("outputs/visuals/remote_index.html")
        return fig

if __name__ == "__main__":
    viz = PJMAVisualizer()
    print("📊 Generating Market Intelligence Visuals...")
    viz.plot_skill_dominance()
    viz.plot_city_distribution()
    viz.plot_experience_heatmap()
    viz.plot_remote_index()
    print("✅ Visuals archived in outputs/visuals/")