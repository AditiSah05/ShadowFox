"""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║                   IPL FIELDING ANALYSIS SYSTEM                             ║
║                          ShadowFox Analytics                               ║
║                                                                            ║
║                        LEARN • CREATE • LEAD                               ║
║                    https://www.shadowfox.org.in/                           ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝

IPL Cricket Fielding Performance Analysis Tool
Based on Performance Score Formula with Weighted Metrics
"""

import pandas as pd
import json
from datetime import datetime
from pathlib import Path


class IPLFieldingAnalyzer:
    """
    IPL Fielding Analysis System
    
    Performance Score Formula:
    PS = (CP×WCP) + (GT×WGT) + (C×WC) + (DC×WDC) + (ST×WST) + 
         (RO×WRO) + (MRO×WMRO) + (DH×WDH) + RS
    
    Weights:
    - WCP: +1 (Clean Picks)
    - WGT: +1 (Good Throws)  
    - WC: +1 (Catches)
    - WDC: -3 (Dropped Catches)
    - WST: +3 (Stumpings)
    - WRO: +3 (Run Outs)
    - WMRO: -2 (Missed Run Outs)
    - WDH: +2 (Direct Hits)
    """
    
    # Weights from the sample calculations
    WEIGHTS = {
        'WCP': 1,    # Clean Picks
        'WGT': 1,    # Good Throws
        'WC': 1,     # Catches
        'WDC': -3,   # Dropped Catches (negative)
        'WST': 3,    # Stumpings
        'WRO': 3,    # Run Outs
        'WMRO': -2,  # Missed Run Outs (negative)
        'WDH': 2     # Direct Hits
    }
    
    def __init__(self):
        """Initialize the analyzer."""
        self.output_dir = Path('cricket_analysis')
        self.output_dir.mkdir(exist_ok=True)
        print(self._banner())
    
    def _banner(self):
        """Return application banner."""
        return """
╔════════════════════════════════════════════════════════════════════════════╗
║                   IPL FIELDING ANALYSIS SYSTEM                             ║
║                          ShadowFox Analytics                               ║
║                        LEARN • CREATE • LEAD                               ║
║                    https://www.shadowfox.org.in/                           ║
╚════════════════════════════════════════════════════════════════════════════╝
"""
    
    def create_sample_data(self):
        """Create sample IPL fielding data matching the Excel format."""
        # Sample Performance Matrix data
        performance_data = {
            'Player_Name': ['Risee russouw', 'Phil Salt', 'Yash Dhull', 'Axer Patel', 'Lalit yadav', 'Aman Khan', 'Kuldeep yadav'],
            'CP': [2, 1, 3, 2, 1, 4, 3],      # Clean Picks
            'GT': [1, 2, 1, 3, 2, 1, 0],      # Good Throws
            'C': [1, 0, 2, 1, 1, 0, 1],       # Catches
            'DC': [0, 1, 0, 0, 0, 0, 1],      # Dropped Catches
            'ST': [0, 0, 0, 0, 0, 0, 0],      # Stumpings
            'RO': [0, 0, 0, 1, 0, 0, 0],      # Run Outs
            'MRO': [1, 0, 0, 0, 0, 0, 0],     # Missed Run Outs
            'DH': [1, 0, 0, 0, 0, 1, 1],      # Direct Hits
            'RS': [3, -1, 3, 0, -2, 1, 4]     # Runs Saved
        }
        
        df = pd.DataFrame(performance_data)
        
        # Calculate Performance Score
        df['PS'] = (
            df['CP'] * self.WEIGHTS['WCP'] +
            df['GT'] * self.WEIGHTS['WGT'] +
            df['C'] * self.WEIGHTS['WC'] +
            df['DC'] * self.WEIGHTS['WDC'] +
            df['ST'] * self.WEIGHTS['WST'] +
            df['RO'] * self.WEIGHTS['WRO'] +
            df['MRO'] * self.WEIGHTS['WMRO'] +
            df['DH'] * self.WEIGHTS['WDH'] +
            df['RS']
        )
        
        return df
    
    def load_from_excel(self, filepath):
        """Load fielding data from Excel file."""
        try:
            df = pd.read_excel(filepath)
            print(f"[OK] Loaded {len(df)} records from {filepath}")
            return df
        except Exception as e:
            print(f"[ERROR] Could not load Excel file: {e}")
            return None
    
    def calculate_performance_score(self, row):
        """Calculate PS for a single player."""
        ps = (
            row['CP'] * self.WEIGHTS['WCP'] +
            row['GT'] * self.WEIGHTS['WGT'] +
            row['C'] * self.WEIGHTS['WC'] +
            row['DC'] * self.WEIGHTS['WDC'] +
            row['ST'] * self.WEIGHTS['WST'] +
            row['RO'] * self.WEIGHTS['WRO'] +
            row['MRO'] * self.WEIGHTS['WMRO'] +
            row['DH'] * self.WEIGHTS['WDH'] +
            row['RS']
        )
        return ps
    
    def analyze_players(self, df):
        """Analyze and rank players by performance score."""
        print("\n" + "=" * 80)
        print("IPL FIELDING PERFORMANCE ANALYSIS")
        print("=" * 80 + "\n")
        
        # Sort by Performance Score
        df_sorted = df.sort_values('PS', ascending=False).reset_index(drop=True)
        
        # Display results
        for idx, row in df_sorted.iterrows():
            print(f"{idx + 1}. {row['Player_Name']}")
            print(f"   Performance Score: {row['PS']:.0f}")
            print(f"   CP={row['CP']}, GT={row['GT']}, C={row['C']}, DC={row['DC']}")
            print(f"   ST={row['ST']}, RO={row['RO']}, MRO={row['MRO']}, DH={row['DH']}, RS={row['RS']:+.0f}")
            
            # Show calculation
            calc = (f"   PS = ({row['CP']}×1) + ({row['GT']}×1) + ({row['C']}×1) + "
                   f"({row['DC']}×-3) + ({row['ST']}×3) + ({row['RO']}×3) + "
                   f"({row['MRO']}×-2) + ({row['DH']}×2) + {row['RS']:+.0f}")
            print(calc)
            print(f"   PS = {row['PS']:.0f}\n")
        
        return df_sorted
    
    def export_results(self, df, filename='ipl_fielding_analysis'):
        """Export results to Excel and JSON."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Export to Excel
        excel_file = self.output_dir / f'{filename}_{timestamp}.xlsx'
        with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Performance Analysis', index=False)
            
            # Add weights sheet
            weights_df = pd.DataFrame([
                {'Metric': 'Clean Picks (CP)', 'Weight': self.WEIGHTS['WCP']},
                {'Metric': 'Good Throws (GT)', 'Weight': self.WEIGHTS['WGT']},
                {'Metric': 'Catches (C)', 'Weight': self.WEIGHTS['WC']},
                {'Metric': 'Dropped Catches (DC)', 'Weight': self.WEIGHTS['WDC']},
                {'Metric': 'Stumpings (ST)', 'Weight': self.WEIGHTS['WST']},
                {'Metric': 'Run Outs (RO)', 'Weight': self.WEIGHTS['WRO']},
                {'Metric': 'Missed Run Outs (MRO)', 'Weight': self.WEIGHTS['WMRO']},
                {'Metric': 'Direct Hits (DH)', 'Weight': self.WEIGHTS['WDH']}
            ])
            weights_df.to_excel(writer, sheet_name='Weights', index=False)
        
        print(f"[OK] Results exported to: {excel_file}")
        
        # Export to JSON
        json_file = self.output_dir / f'{filename}_{timestamp}.json'
        results = {
            'analysis_date': datetime.now().isoformat(),
            'weights': self.WEIGHTS,
            'players': df.to_dict('records')
        }
        
        with open(json_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"[OK] Results exported to: {json_file}")
    
    def generate_report(self, df, filename='ipl_fielding_report'):
        """Generate text report."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.output_dir / f'{filename}_{timestamp}.txt'
        
        with open(report_file, 'w') as f:
            f.write("=" * 80 + "\n")
            f.write("IPL FIELDING PERFORMANCE ANALYSIS REPORT\n")
            f.write("ShadowFox Analytics\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")
            
            f.write("PERFORMANCE SCORE FORMULA:\n")
            f.write("-" * 80 + "\n")
            f.write("PS = (CP×WCP) + (GT×WGT) + (C×WC) + (DC×WDC) + (ST×WST) +\n")
            f.write("     (RO×WRO) + (MRO×WMRO) + (DH×WDH) + RS\n\n")
            
            f.write("WEIGHTS:\n")
            f.write("-" * 80 + "\n")
            for key, value in self.WEIGHTS.items():
                f.write(f"{key}: {value:+d}\n")
            f.write("\n")
            
            f.write("PLAYER RANKINGS:\n")
            f.write("-" * 80 + "\n\n")
            
            for idx, row in df.iterrows():
                f.write(f"{idx + 1}. {row['Player_Name']}\n")
                f.write(f"   Performance Score: {row['PS']:.0f}\n")
                f.write(f"   Catches: {row['C']}, Run Outs: {row['RO']}, Direct Hits: {row['DH']}\n")
                f.write(f"   Runs Impact: {row['RS']:+.0f}\n\n")
            
            f.write("=" * 80 + "\n")
            f.write("KEY INSIGHTS:\n")
            f.write("-" * 80 + "\n")
            
            best = df.iloc[0]
            f.write(f"• Best Performer: {best['Player_Name']} (PS: {best['PS']:.0f})\n")
            
            most_catches = df.loc[df['C'].idxmax()]
            f.write(f"• Most Catches: {most_catches['Player_Name']} ({most_catches['C']:.0f} catches)\n")
            
            if df['RO'].max() > 0:
                most_runouts = df.loc[df['RO'].idxmax()]
                f.write(f"• Most Run Outs: {most_runouts['Player_Name']} ({most_runouts['RO']:.0f} run outs)\n")
            
            f.write("\n" + "=" * 80 + "\n")
        
        print(f"[OK] Report generated: {report_file}")


def main():
    """Main function."""
    analyzer = IPLFieldingAnalyzer()
    
    # Create sample data
    print("[INFO] Creating sample IPL fielding data...")
    df = analyzer.create_sample_data()
    
    # Save sample data
    sample_file = analyzer.output_dir / 'sample_ipl_data.xlsx'
    df.to_excel(sample_file, index=False)
    print(f"[OK] Sample data saved to: {sample_file}\n")
    
    # Analyze players
    df_analyzed = analyzer.analyze_players(df)
    
    # Display summary table
    print("=" * 80)
    print("SUMMARY TABLE")
    print("=" * 80)
    print(df_analyzed[['Player_Name', 'PS', 'C', 'RO', 'DH', 'RS']].to_string(index=False))
    print("=" * 80 + "\n")
    
    # Export results
    analyzer.export_results(df_analyzed)
    analyzer.generate_report(df_analyzed)
    
    print("\n[OK] Analysis complete!")


if __name__ == "__main__":
    main()
