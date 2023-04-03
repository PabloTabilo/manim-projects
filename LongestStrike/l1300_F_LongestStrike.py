from manim import *

class SolveLongestStrike(Scene):
    def construct(self):
        title = Tex(r"F Longest Strike", font_size=25)
        def_inputs = Tex(r"Given an array of size n:  $a[n]$ and integer $k$",font_size=21)
        def_task = Tex(r"The task is find any two numbers $l$ and $r$ (where $l \le r$) such that:",font_size=21)

        pGroup = VGroup(title,def_inputs,def_task).arrange(DOWN)
        
        ite1 = r"$\forall x \in l \le x \le r $, $x$ appears in $a$ at least $k$"
        ite2 = r"$ \max \{r-l\} $"
        blist = BulletedList(ite1, ite2,font_size=21)

        bgr = VGroup(blist).arrange(DOWN)
        
        bgr.next_to(pGroup,DOWN)

        self.play(FadeIn(pGroup))
        self.wait()
        self.play(FadeIn(bgr))
        self.wait()
        self.play(FadeOut(pGroup),FadeOut(bgr))
        
        ext = Title("Example")
        self.play(Write(ext))

        ex = MathTex("\{","14","\\ 11","\\ 13", "\\ 13", "\\ 12", "\\ 11", "\\ 14","\}") 
        self.play(Write(ex))

        extexs=Tex(r"Need sort this! Use mergeSort $O(n \log n)$, radixSort $O(d \cdot n)$, data-structure (bst) $O(n \log n)$, etc.", font_size=20)
        
        extexs.next_to(ex,DOWN)
        self.play(Write(extexs))
        f1 = SurroundingRectangle(ex[1], buff = .1)
        f2 = SurroundingRectangle(ex[7], buff = .1)
        
        self.play(Create(f1))
        self.wait()
        self.play(ReplacementTransform(f1,f2))
        self.wait()
        self.play(FadeOut(ex),FadeOut(f1),FadeOut(f2), FadeOut(extexs)) 

        exs = MathTex("\{","11","\\ 11","\\ 12", "\\ 13", "\\ 13", "\\ 14", "\\ 14","\}") 
        self.play(Write(exs))
        
        l = SurroundingRectangle(exs[1], buff = .1, color="#7291FF")
        r = SurroundingRectangle(exs[2], buff = .1, color="#86EF79")

        kt = Tex("$k=2$",font_size=30)
        kt.next_to(exs)
        
        self.play(Create(l), Create(r), Write(kt))
        
        purt = Tex(r"if $\forall x \in [ l=11,r=11 ]$ \& $ frequencies(x) \ge k $",font_size=30)
        purt.next_to(exs,DOWN)
        self.play(Write(purt))
        resf = Tex("Yes, $res = 11-11 = 0$", font_size=25, color="green")
        resf.next_to(exs,UP) 
        self.play(Write(resf))
        self.wait()
        self.play(FadeOut(purt))

        rn = SurroundingRectangle(exs[3], buff = .1, color="#86EF79")
        self.play(ReplacementTransform(r,rn))
        
        purt = Tex(r"if $\forall x \in [ l=11,r=12 ]$ \& $ frequencies(x) \ge k $",font_size=30)
        purt.next_to(exs,DOWN)
        self.play(Write(purt),FadeOut(resf))
        resf=Tex("$res=11-11=0$",color="green")
        resf.next_to(exs,UP) 
        self.play(FadeIn(resf))
        res = Tex("NO, $12$ exist only once", font_size=25, color="red")
        res.next_to(purt,DOWN) 
        self.play(Write(res))
        self.wait()
        self.play(FadeOut(purt),FadeOut(res))
        
        ln = SurroundingRectangle(exs[4], buff = .1, color="#7291FF")
        r = SurroundingRectangle(exs[7], buff = .1, color="#86EF79")
        self.play(ReplacementTransform(l,ln),ReplacementTransform(rn,r))

        purt = Tex(r"if $\forall x \in [ l=13,r=14 ]$ \& $ frequencies(x) \ge k $",font_size=30)
        purt.next_to(exs,DOWN)
        self.play(Write(purt),FadeOut(resf))
        resf = Tex("$res = 14-13 = 1$", font_size=25, color="green")
        resf.next_to(exs,UP) 
        self.play(Write(resf))
        self.wait()
        self.play(FadeOut(ext),FadeOut(purt),FadeOut(ln),FadeOut(r),FadeOut(resf),FadeOut(exs),FadeOut(kt))
        
        self.solution_code()

    def solution_code(self):
        title = Title("Possible Solution",font_size=20) 
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
                    if(l!=-1){
                        r=x.first;
                    }else{
                        l=r=x.first;
                    }
                    p_adj=x.first;
                }else{
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
            if(l!=-1&&r!=-1&&diff<abs(r-l)){
                bl=l;
                br=r;
                diff=abs(r-l);
            }
            if(bl==-1&&br==-1) cout<<bl<<endl;
            else cout<<bl<<" "<<br<<endl;
        }
        '''
        rendered_code = Code(code=code,tab_width=4, background="window",language="cpp",font_size=8)
        self.play(Write(title),FadeIn(rendered_code))
        self.wait() 
        self.play(FadeOut(title),FadeOut(rendered_code))

        self.code_inputs_and_map()
        self.define_principal_vars_track()
        self.explain_principal_logic()
        self.last_if()
        self.get_ans()

    def get_ans(self):
        title = Title("Final Ans",font_size=20)
        code='''
        if(bl==-1&&br==-1) cout<<bl<<endl;
        else cout<<bl<<" "<<br<<endl;
        '''
        rendered_code = Code(code=code,tab_width=4, background="window",language="cpp",font_size=14)
        it1 = r"If $bl=-1$ and $br=-1$ this mean that not exist a possible solution (every $frequencies(x) < k$) print -1"
        it2 = r"Otherwise, print $bl$ and $br$"
        bl = BulletedList(it1,it2,font_size=18)
        gr = VGroup(rendered_code,bl).arrange(DOWN)
        self.play(Write(title),FadeIn(gr))
        self.wait()
        self.play(FadeOut(gr),FadeOut(title))

    def last_if(self):
        title = Title("The inmediate block code after iterate map",font_size=20)
        code = '''
        // check if ans can update
            if(l!=-1&&r!=-1&&diff<abs(r-l)){
                bl=l;
                br=r;
                diff=abs(r-l);
            }
        '''
        rendered_code = Code(code=code,tab_width=4, background="window",language="cpp",font_size=14)
        it1 = r"Check if the last ans is not save"
        it2 = r"This can happen if we get factibles numbers from $k$ position to $n$ or last element, so we need to check if this ans is the best ans"
        bl = BulletedList(it1,it2,font_size=18)
        gr = VGroup(rendered_code,bl).arrange(DOWN)
        self.play(Write(title),FadeIn(gr))
        self.wait()
        self.play(FadeOut(gr),FadeOut(title))

    def explain_principal_logic_else(self):
        title = Title("5. Analyze else",font_size=20) 
        self.play(Write(title))
        code = '''
            else{
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

        '''
        rendered_code = Code(code=code,tab_width=4, background="window",language="cpp",font_size=14)
        it1 = r"Case that's not a factible case"
        bl = BulletedList(it1,font_size=18)
        gr = VGroup(rendered_code,bl).arrange(DOWN)
        self.play(FadeIn(gr))
        self.wait()
        self.play(FadeOut(gr))

        code = '''
                if(r!=-1&&l!=-1&&diff<abs(r-l)){
                    bl=l;
                    br=r;
                    diff=abs(r-l);
                }
        '''
        rendered_code = Code(code=code,tab_width=4, background="window",language="cpp",font_size=14)
        it1 = r"Save the current ans $r-l$ because is better than current best ans $diff$ at the moment"
        bl = BulletedList(it1,font_size=18)
        gr = VGroup(rendered_code,bl).arrange(DOWN)
        self.play(FadeIn(gr))
        self.wait()
        self.play(FadeOut(gr))

        code = '''
                if(x.second>=k){
                    l=r=x.first;
                    p_adj=x.first;
                }else{
                    l=r=-1;
                }
        '''
        rendered_code = Code(code=code,tab_width=4, background="window",language="cpp",font_size=14)
        it1 = r"If current x.second is bigger or equal than k, update $l$, $r$, and previous $p_{adj}$ because can be new pottencial range of $r - l$"
        it2 = r"Otherwise, reboot $l$ and $r$, because the current x.first not accomplish be more than $k$"
        bl = BulletedList(it1,it2,font_size=18)
        gr = VGroup(rendered_code,bl).arrange(DOWN)
        self.play(FadeIn(gr))
        self.wait()
        self.play(FadeOut(gr),FadeOut(title))
    
    def explain_principal_logic_if(self):
        title = Title("4. Analyze if",font_size=20) 
        self.play(Write(title))
        code_first_part='''
            if((abs(x.first-p_adj)==1||p_adj==-1) && x.second>=k){
                //get ans
                if(l!=-1){
                    r=x.first;
                }else{
                    l=r=x.first;
                }
                p_adj=x.first;
            }
        '''
        rendered_code = Code(code=code_first_part,tab_width=4, background="window",language="cpp",font_size=11)
        it1 = r"This if represent that is a factible value for aggregate on the answer, and can update $l$ and $r$ or only $r$"
        it2 = r"if $l \neq -1$ that's mean that $l$ exist like a possible ans, so we need only update $r$"
        it3 = r"Otherwise, we need to update $l$ and $r$"
        it4 = r"$p_{adj}$: Check adjancecy between $a[i]$ elements, where the diff must be 1, that's mean $pointer_{1,ref} - pointer_{2,ref} = 1$ or $a[i] - a[i-1]=1$"
        it5 = r"For the previous reason we need to update $p_{adj}$ with the current x.first for analyze if this is adjacenty to the next val"
        bl = BulletedList(it1,it2,it3,it4,it5,font_size=18)
        
        gr = VGroup(rendered_code,bl).arrange(DOWN)
        
        self.play(FadeIn(gr))
        self.wait()
        self.play(FadeOut(gr),FadeOut(title))

    def explain_principal_logic(self):
        title = Title("3. Iterate over data-structure",font_size=20) 
        self.play(Write(title))
        code = '''
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
        '''
        rendered_code = Code(code=code,tab_width=4, background="window",language="cpp",font_size=11)
        it1 = r"$x$ is a iterator of the $map$"
        it2 = r"So $x$ is a pair, where x.first store $a[i]$ and x.second store frequency"
        bl = BulletedList(it1,it2,font_size=18)

        gr = VGroup(rendered_code,bl).arrange(DOWN)
        
        self.play(FadeIn(gr))
        self.wait()
        self.play(FadeOut(gr),FadeOut(title))
        
        self.explain_principal_logic_if()
        self.explain_principal_logic_else()
        
    def define_principal_vars_track(self):
        title = Title("2. Variables definitions for apply solution",font_size=20) 
        self.play(Write(title))
        code = '''
            int l=-1,r=-1;
            int diff=-1, bl=-1,br=-1;
            int p_adj=-1;
        '''
        rendered_code = Code(code=code,tab_width=4, background="window",language="cpp",font_size=14)
        
        it1 = r"$l$ and $r$ are the current value that's analyze, $l=a[i]$ and $r=a[i+k]$"
        it2 = r"$diff$ : maintain the best ans for $r-l$"
        it3 = r"$bl$ : best $l$ value" 
        it4 = r"$br$: best $r$ value"
        it5 = r"$p_{adj}$: Check adjancecy between $a[i]$ elements, where the diff must be 1, that's mean $pointer_{1,ref} - pointer_{2,ref} = 1$ or $a[i] - a[i-1]=1$"
        bl = BulletedList(it1,it2,it3,it4,it5,font_size=18)

        gr = VGroup(rendered_code,bl).arrange(DOWN)
        
        self.play(FadeIn(gr))
        self.wait()
        self.play(FadeOut(gr),FadeOut(title))


    def code_inputs_and_map(self):
        title = Title("1. Inputs and data-structure",font_size=20) 
        self.play(Write(title))
        code = '''
            int n, k;
            cin>>n>>k;
            vector<int>a(n);
            map<int,int> f;
            for(int i=0;i<n;i++){
                cin>>a[i];
                f[a[i]]++;
            }
        '''
        rendered_code = Code(code=code,tab_width=4, background="window",language="cpp",font_size=14)
        
        it1 = r"Define integer $n$, $k$ and a vector of size $n$ call $a$, all this for read inputs"
        it2 = r"Create a map data structure (implemented as BST), where the pair ($key$,$value$) are define as integers"
        it3 = r"The objective of map is capture the frequency (value) of each integer $a[i]$ (key) and sort them, because need maintain bst invariant"
        bl = BulletedList(it1, it2, it3,font_size=18)
        gr = VGroup(rendered_code,bl).arrange(DOWN)
        self.play(FadeIn(gr))
        self.wait()
        self.play(FadeOut(gr), FadeOut(title))




