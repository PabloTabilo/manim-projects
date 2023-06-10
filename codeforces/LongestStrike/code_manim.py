from manim import *

class CodeFromString(Scene):
    def construct(self):
        code = '''
void solve(){
    int n, k;
    cin>>n>>k;
    vector<int>a(n);
    map<int,int> f;
    for(int i=0;i<n;i++){
        cin>>a[i];
        f[a[i]]++;
    }
    int l=-1,r=-1;
    int diff=-1, bl=-1,br=-1;
    int p_adj=-1;
    for(auto x : f){
        if((abs(x.first-p_adj)==1||p_adj==-1) && x.second>=k){
            //get ans
            if(l!=-1){
                r=x.first;
            }else{
                l=r=x.first;
            }
            p_adj=x.first;
        }else{
            //reset and save best ans
            if(r!=-1&&l!=-1&&diff<abs(r-l)){
                bl=l;
                br=r;
                diff=abs(r-l);
            }
            if(x.second>=k){
                l=r=x.first;
                p_adj=x.first;
            }else{
                l=r=-1;
            }
        }
    }
    // check if ans can update
    if(l!=-1&&r!=-1&&diff<abs(r-l)){
        bl=l;
        br=r;
        diff=abs(r-l);
    }
    if(bl==-1&&br==-1) cout<<bl<<endl;
    else cout<<bl<<" "<<br<<endl;
}
'''
        rendered_code = Code(code=code, tab_width=4, background="window",
                            language="cpp", font="Monospace",font_size=11)
        self.play(FadeIn(rendered_code))
