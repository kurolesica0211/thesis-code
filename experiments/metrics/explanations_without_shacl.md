14_14
- ObjectPropertyAssertion(<http://example.com/family_TBOX.ttl#isChildOf> <http://example.org/data/LilibetDianaMountbattenWindsor> <http://example.org/data/PrinceArchie>)
- ObjectPropertyAssertion(<http://example.com/family_TBOX.ttl#isBrotherOf> <http://example.org/data/PrinceArchie> <http://example.org/data/LilibetDianaMountbattenWindsor>)
- DisjointObjectProperties(<http://example.com/family_TBOX.ttl#hasBrother> <http://example.com/family_TBOX.ttl#isChildOf> )
- InverseObjectProperties(<http://example.com/family_TBOX.ttl#hasBrother> <http://example.com/family_TBOX.ttl#isBrotherOf>)

37_37
- ObjectPropertyDomain(<http://example.com/family_TBOX.ttl#isBrotherOf> <http://example.com/family_TBOX.ttl#Man>)
- ObjectPropertyAssertion(<http://example.com/family_TBOX.ttl#isBrotherOf> <http://example.org/data/Maria_de_las_Mercedes> <http://example.org/data/Alfonso_XIII>)
- DisjointClasses(<http://example.com/family_TBOX.ttl#Man> <http://example.com/family_TBOX.ttl#Woman>)
- ClassAssertion(<http://example.com/family_TBOX.ttl#Woman> <http://example.org/data/Maria_de_las_Mercedes>)

46_46
- SubObjectPropertyOf(<http://example.com/family_TBOX.ttl#hasMother> <http://example.com/family_TBOX.ttl#hasParent>)
- ClassAssertion(<http://example.com/family_TBOX.ttl#Woman> <http://example.org/data/Zara_Tindall>)
- ObjectPropertyAssertion(<http://example.com/family_TBOX.ttl#hasMother> <http://example.org/data/Anne_Princess_Royal> <http://example.org/data/Queen_Elizabeth_II>)
- ObjectPropertyAssertion(<http://example.com/family_TBOX.ttl#hasMother> <http://example.org/data/Zara_Tindall> <http://example.org/data/Anne_Princess_Royal>)
- ObjectPropertyAssertion(<http://example.com/family_TBOX.ttl#hasMother> <http://example.org/data/Zara_Tindall> <http://example.org/data/Queen_Elizabeth_II>)
- DLSafeRule(Annotation(<http://swrl.stanford.edu/ontologies/3.3/swrla.owl#isRuleEnabled> "true"^^xsd:boolean) Annotation(rdfs:comment "") Annotation(rdfs:label "infer hasSister")  Body(ClassAtom(<http://example.com/family_TBOX.ttl#Woman> Variable(<http://example.com/family_TBOX.ttl#y>)) ObjectPropertyAtom(<http://example.com/family_TBOX.ttl#isSiblingOf> Variable(<http://example.com/family_TBOX.ttl#x>) Variable(<http://example.com/family_TBOX.ttl#y>))) Head(ObjectPropertyAtom(<http://example.com/family_TBOX.ttl#hasSister> Variable(<http://example.com/family_TBOX.ttl#x>) Variable(<http://example.com/family_TBOX.ttl#y>))) )
- DisjointObjectProperties(<http://example.com/family_TBOX.ttl#hasSister> <http://example.com/family_TBOX.ttl#isParentOf> )
- SubObjectPropertyOf(ObjectPropertyChain( <http://example.com/family_TBOX.ttl#hasParent> <http://example.com/family_TBOX.ttl#isParentOf> ) <http://example.com/family_TBOX.ttl#isSiblingOf>)
- InverseObjectProperties(<http://example.com/family_TBOX.ttl#hasParent> <http://example.com/family_TBOX.ttl#isParentOf>)

61_61
- SubObjectPropertyOf(<http://example.com/family_TBOX.ttl#hasMother> <http://example.com/family_TBOX.ttl#hasParent>)
- ObjectPropertyAssertion(<http://example.com/family_TBOX.ttl#hasMother> <http://example.org/data/Willem-Alexander> <http://example.org/data/Juliana>)
- ObjectPropertyAssertion(<http://example.com/family_TBOX.ttl#hasMother> <http://example.org/data/Beatrix> <http://example.org/data/Juliana>)
- ClassAssertion(<http://example.com/family_TBOX.ttl#Man> <http://example.org/data/Willem-Alexander>)
- ObjectPropertyAssertion(<http://example.com/family_TBOX.ttl#hasMother> <http://example.org/data/Willem-Alexander> <http://example.org/data/Beatrix>)
- SubObjectPropertyOf(ObjectPropertyChain( <http://example.com/family_TBOX.ttl#hasParent> <http://example.com/family_TBOX.ttl#isParentOf> ) <http://example.com/family_TBOX.ttl#isSiblingOf>)
- DisjointObjectProperties(<http://example.com/family_TBOX.ttl#hasBrother> <http://example.com/family_TBOX.ttl#isParentOf> )
- InverseObjectProperties(<http://example.com/family_TBOX.ttl#hasParent> <http://example.com/family_TBOX.ttl#isParentOf>)
- DLSafeRule(Annotation(<http://swrl.stanford.edu/ontologies/3.3/swrla.owl#isRuleEnabled> "true"^^xsd:boolean) Annotation(rdfs:comment "") Annotation(rdfs:label "infer hasBrother")  Body(ClassAtom(<http://example.com/family_TBOX.ttl#Man> Variable(<http://example.com/family_TBOX.ttl#y>)) ObjectPropertyAtom(<http://example.com/family_TBOX.ttl#isSiblingOf> Variable(<http://example.com/family_TBOX.ttl#x>) Variable(<http://example.com/family_TBOX.ttl#y>))) Head(ObjectPropertyAtom(<http://example.com/family_TBOX.ttl#hasBrother> Variable(<http://example.com/family_TBOX.ttl#x>) Variable(<http://example.com/family_TBOX.ttl#y>))) )

77_77
- ObjectPropertyAssertion(<http://example.com/family_TBOX.ttl#isMotherOf> <http://example.org/data/George_von_dem_Bussche-Haddenhausen> <http://example.org/data/Baroness_G%C3%B6sta_von_dem_Bussche-Haddenhausen>)
- ClassAssertion(<http://example.com/family_TBOX.ttl#Man> <http://example.org/data/George_von_dem_Bussche-Haddenhausen>)
- DisjointClasses(<http://example.com/family_TBOX.ttl#Man> <http://example.com/family_TBOX.ttl#Woman>)
- ObjectPropertyDomain(<http://example.com/family_TBOX.ttl#isMotherOf> <http://example.com/family_TBOX.ttl#Woman>)

98_98
- ObjectPropertyAssertion(<http://example.com/family_TBOX.ttl#hasChild> <http://example.org/data/Princess_Beatrix> <http://example.org/data/Prince_Claus>)
- ClassAssertion(<http://example.com/family_TBOX.ttl#Man> <http://example.org/data/Prince_Claus>)
- InverseObjectProperties(<http://example.com/family_TBOX.ttl#hasChild> <http://example.com/family_TBOX.ttl#isChildOf>)
- ObjectPropertyAssertion(<http://example.com/family_TBOX.ttl#hasChild> <http://example.org/data/Prince_Claus> <http://example.org/data/Prince_Constantijn>)
- EquivalentObjectProperties(<http://example.com/family_TBOX.ttl#hasParent> <http://example.com/family_TBOX.ttl#isChildOf> )
- ObjectPropertyAssertion(<http://example.com/family_TBOX.ttl#hasChild> <http://example.org/data/Princess_Beatrix> <http://example.org/data/Prince_Constantijn>)
- DisjointObjectProperties(<http://example.com/family_TBOX.ttl#hasBrother> <http://example.com/family_TBOX.ttl#isChildOf> )
- SubObjectPropertyOf(ObjectPropertyChain( <http://example.com/family_TBOX.ttl#hasParent> <http://example.com/family_TBOX.ttl#isParentOf> ) <http://example.com/family_TBOX.ttl#isSiblingOf>)
- InverseObjectProperties(<http://example.com/family_TBOX.ttl#hasParent> <http://example.com/family_TBOX.ttl#isParentOf>)
- DLSafeRule(Annotation(<http://swrl.stanford.edu/ontologies/3.3/swrla.owl#isRuleEnabled> "true"^^xsd:boolean) Annotation(rdfs:comment "") Annotation(rdfs:label "infer hasBrother")  Body(ClassAtom(<http://example.com/family_TBOX.ttl#Man> Variable(<http://example.com/family_TBOX.ttl#y>)) ObjectPropertyAtom(<http://example.com/family_TBOX.ttl#isSiblingOf> Variable(<http://example.com/family_TBOX.ttl#x>) Variable(<http://example.com/family_TBOX.ttl#y>))) Head(ObjectPropertyAtom(<http://example.com/family_TBOX.ttl#hasBrother> Variable(<http://example.com/family_TBOX.ttl#x>) Variable(<http://example.com/family_TBOX.ttl#y>))) )

106_106
- ObjectPropertyAssertion(<http://example.com/family_TBOX.ttl#hasFather> <http://example.org/data/Louis_Alphonse_de_Bourbon> <http://example.org/data/Louis_Alphonse_de_Bourbon>)
- ObjectPropertyRange(<http://example.com/family_TBOX.ttl#hasFather> <http://example.com/family_TBOX.ttl#Man>)
- SubObjectPropertyOf(<http://example.com/family_TBOX.ttl#hasFather> <http://example.com/family_TBOX.ttl#hasParent>)
- SubObjectPropertyOf(ObjectPropertyChain( <http://example.com/family_TBOX.ttl#hasParent> <http://example.com/family_TBOX.ttl#isParentOf> ) <http://example.com/family_TBOX.ttl#isSiblingOf>)
- DisjointObjectProperties(<http://example.com/family_TBOX.ttl#hasBrother> <http://example.com/family_TBOX.ttl#isParentOf> )
- InverseObjectProperties(<http://example.com/family_TBOX.ttl#hasParent> <http://example.com/family_TBOX.ttl#isParentOf>)
- DLSafeRule(Annotation(<http://swrl.stanford.edu/ontologies/3.3/swrla.owl#isRuleEnabled> "true"^^xsd:boolean) Annotation(rdfs:comment "") Annotation(rdfs:label "infer hasBrother")  Body(ClassAtom(<http://example.com/family_TBOX.ttl#Man> Variable(<http://example.com/family_TBOX.ttl#y>)) ObjectPropertyAtom(<http://example.com/family_TBOX.ttl#isSiblingOf> Variable(<http://example.com/family_TBOX.ttl#x>) Variable(<http://example.com/family_TBOX.ttl#y>))) Head(ObjectPropertyAtom(<http://example.com/family_TBOX.ttl#hasBrother> Variable(<http://example.com/family_TBOX.ttl#x>) Variable(<http://example.com/family_TBOX.ttl#y>))) )

117_117
- ObjectPropertyAssertion(<http://example.com/family_TBOX.ttl#hasMother> <http://example.org/data/QueenSofia> <http://example.org/data/KingPaulOfGreece>)
- DisjointClasses(<http://example.com/family_TBOX.ttl#Man> <http://example.com/family_TBOX.ttl#Woman>)
- ObjectPropertyRange(<http://example.com/family_TBOX.ttl#hasMother> <http://example.com/family_TBOX.ttl#Woman>)
- ClassAssertion(<http://example.com/family_TBOX.ttl#Man> <http://example.org/data/KingPaulOfGreece>)

133_133
- InverseObjectProperties(<http://example.com/family_TBOX.ttl#hasChild> <http://example.com/family_TBOX.ttl#isChildOf>)
- ObjectPropertyDomain(<http://example.com/family_TBOX.ttl#isFatherOf> <http://example.com/family_TBOX.ttl#Man>)
- ObjectPropertyAssertion(<http://example.com/family_TBOX.ttl#isMotherOf> <http://example.org/data/Rose_Leveson-Gower_Countess_Granville> <http://example.org/data/Granville_Leveson-Gower_5th_Earl_Granville>)
- ObjectPropertyAssertion(<http://example.com/family_TBOX.ttl#isMotherOf> <http://example.org/data/Rose_Leveson-Gower_Countess_Granville> <http://example.org/data/Granville_George_Fergus_Leveson-Gower>)
- DisjointObjectProperties(<http://example.com/family_TBOX.ttl#hasBrother> <http://example.com/family_TBOX.ttl#isChildOf> )
- SubObjectPropertyOf(ObjectPropertyChain( <http://example.com/family_TBOX.ttl#hasParent> <http://example.com/family_TBOX.ttl#isParentOf> ) <http://example.com/family_TBOX.ttl#isSiblingOf>)
- ObjectPropertyAssertion(<http://example.com/family_TBOX.ttl#isFatherOf> <http://example.org/data/Granville_Leveson-Gower_5th_Earl_Granville> <http://example.org/data/Granville_George_Fergus_Leveson-Gower>)
- InverseObjectProperties(<http://example.com/family_TBOX.ttl#hasParent> <http://example.com/family_TBOX.ttl#isParentOf>)
- SubObjectPropertyOf(<http://example.com/family_TBOX.ttl#isFatherOf> <http://example.com/family_TBOX.ttl#hasChild>)
- SubObjectPropertyOf(<http://example.com/family_TBOX.ttl#isMotherOf> <http://example.com/family_TBOX.ttl#isParentOf>)
- DLSafeRule(Annotation(<http://swrl.stanford.edu/ontologies/3.3/swrla.owl#isRuleEnabled> "true"^^xsd:boolean) Annotation(rdfs:comment "") Annotation(rdfs:label "infer hasBrother")  Body(ClassAtom(<http://example.com/family_TBOX.ttl#Man> Variable(<http://example.com/family_TBOX.ttl#y>)) ObjectPropertyAtom(<http://example.com/family_TBOX.ttl#isSiblingOf> Variable(<http://example.com/family_TBOX.ttl#x>) Variable(<http://example.com/family_TBOX.ttl#y>))) Head(ObjectPropertyAtom(<http://example.com/family_TBOX.ttl#hasBrother> Variable(<http://example.com/family_TBOX.ttl#x>) Variable(<http://example.com/family_TBOX.ttl#y>))) )

144_144
- ObjectPropertyAssertion(<http://example.com/family_TBOX.ttl#isBrotherOf> <http://example.org/data/Princess_Sophie_of_Greece_and_Denmark> <http://example.org/data/Prince_Philip_of_Greece_and_Denmark>)
- ObjectPropertyDomain(<http://example.com/family_TBOX.ttl#isBrotherOf> <http://example.com/family_TBOX.ttl#Man>)
- DisjointClasses(<http://example.com/family_TBOX.ttl#Man> <http://example.com/family_TBOX.ttl#Woman>)
- ClassAssertion(<http://example.com/family_TBOX.ttl#Woman> <http://example.org/data/Princess_Sophie_of_Greece_and_Denmark>)

158_158
- ClassAssertion(<http://example.com/family_TBOX.ttl#Man> <http://example.org/data/DmitriPavlovich>)
- ObjectPropertyAssertion(<http://example.com/family_TBOX.ttl#hasMother> <http://example.org/data/AlexandraGeorgievna> <http://example.org/data/DmitriPavlovich>)
- DisjointClasses(<http://example.com/family_TBOX.ttl#Man> <http://example.com/family_TBOX.ttl#Woman>)
- ObjectPropertyRange(<http://example.com/family_TBOX.ttl#hasMother> <http://example.com/family_TBOX.ttl#Woman>)

160_160
- ObjectPropertyRange(<http://example.com/family_TBOX.ttl#hasFather> <http://example.com/family_TBOX.ttl#Man>)
- ObjectPropertyAssertion(<http://example.com/family_TBOX.ttl#hasFather> <http://example.org/data/Georg_Donatus> <http://example.org/data/Cecilie_of_Greece_and_Denmark>)
- ClassAssertion(<http://example.com/family_TBOX.ttl#Woman> <http://example.org/data/Cecilie_of_Greece_and_Denmark>)
- DisjointClasses(<http://example.com/family_TBOX.ttl#Man> <http://example.com/family_TBOX.ttl#Woman>)

164_164
- DisjointClasses(<http://example.com/family_TBOX.ttl#Man> <http://example.com/family_TBOX.ttl#Woman>)
- ObjectPropertyAssertion(<http://example.com/family_TBOX.ttl#hasSister> <http://example.org/data/Alexandra_Feodorovna_Tsarina> <http://example.org/data/Ernest_Louis_of_Hesse>)
- ObjectPropertyRange(<http://example.com/family_TBOX.ttl#hasSister> <http://example.com/family_TBOX.ttl#Woman>)
- ClassAssertion(<http://example.com/family_TBOX.ttl#Man> <http://example.org/data/Ernest_Louis_of_Hesse>)

172_172
- SubObjectPropertyOf(<http://example.com/family_TBOX.ttl#hasFather> <http://example.com/family_TBOX.ttl#hasParent>)
- ObjectPropertyAssertion(<http://example.com/family_TBOX.ttl#hasFather> <http://example.org/data/Lady_Margarita_Armstrong-Jones> <http://example.org/data/Viscount_Linley_brother>)
- ObjectPropertyAssertion(<http://example.com/family_TBOX.ttl#hasSister> <http://example.org/data/Viscount_Linley_brother> <http://example.org/data/Lady_Margarita_Armstrong-Jones>)
- DisjointObjectProperties(<http://example.com/family_TBOX.ttl#hasSister> <http://example.com/family_TBOX.ttl#isParentOf> )
- InverseObjectProperties(<http://example.com/family_TBOX.ttl#hasParent> <http://example.com/family_TBOX.ttl#isParentOf>)

263_263
- SubObjectPropertyOf(<http://example.com/family_TBOX.ttl#hasMother> <http://example.com/family_TBOX.ttl#hasParent>)
- ObjectPropertyAssertion(<http://example.com/family_TBOX.ttl#hasMother> <http://example.org/data/PrinceFriso> <http://example.org/data/QueenBeatrix>)
- ObjectPropertyAssertion(<http://example.com/family_TBOX.ttl#hasMother> <http://example.org/data/QueenBeatrix> <http://example.org/data/QueenJuliana>)
- ClassAssertion(<http://example.com/family_TBOX.ttl#Man> <http://example.org/data/PrinceFriso>)
- ObjectPropertyAssertion(<http://example.com/family_TBOX.ttl#hasMother> <http://example.org/data/PrinceFriso> <http://example.org/data/QueenJuliana>)
- SubObjectPropertyOf(ObjectPropertyChain( <http://example.com/family_TBOX.ttl#hasParent> <http://example.com/family_TBOX.ttl#isParentOf> ) <http://example.com/family_TBOX.ttl#isSiblingOf>)
- DisjointObjectProperties(<http://example.com/family_TBOX.ttl#hasBrother> <http://example.com/family_TBOX.ttl#isParentOf> )
- InverseObjectProperties(<http://example.com/family_TBOX.ttl#hasParent> <http://example.com/family_TBOX.ttl#isParentOf>)
- DLSafeRule(Annotation(<http://swrl.stanford.edu/ontologies/3.3/swrla.owl#isRuleEnabled> "true"^^xsd:boolean) Annotation(rdfs:comment "") Annotation(rdfs:label "infer hasBrother")  Body(ClassAtom(<http://example.com/family_TBOX.ttl#Man> Variable(<http://example.com/family_TBOX.ttl#y>)) ObjectPropertyAtom(<http://example.com/family_TBOX.ttl#isSiblingOf> Variable(<http://example.com/family_TBOX.ttl#x>) Variable(<http://example.com/family_TBOX.ttl#y>))) Head(ObjectPropertyAtom(<http://example.com/family_TBOX.ttl#hasBrother> Variable(<http://example.com/family_TBOX.ttl#x>) Variable(<http://example.com/family_TBOX.ttl#y>))) )

333_333
- ObjectPropertyDomain(<http://example.com/family_TBOX.ttl#isSisterOf> <http://example.com/family_TBOX.ttl#Woman>)
- ClassAssertion(<http://example.com/family_TBOX.ttl#Man> <http://example.org/data/Constantine_II_of_Greece>)
- ObjectPropertyAssertion(<http://example.com/family_TBOX.ttl#isSisterOf> <http://example.org/data/Constantine_II_of_Greece> <http://example.org/data/Queen_Sofia_of_Spain>)
- DisjointClasses(<http://example.com/family_TBOX.ttl#Man> <http://example.com/family_TBOX.ttl#Woman>)

344_344
- ClassAssertion(<http://example.com/family_TBOX.ttl#Man> <http://example.org/data/PrinceMichaelOfGreeceAndDenmark>)
- DisjointClasses(<http://example.com/family_TBOX.ttl#Man> <http://example.com/family_TBOX.ttl#Woman>)
- ObjectPropertyDomain(<http://example.com/family_TBOX.ttl#isMotherOf> <http://example.com/family_TBOX.ttl#Woman>)
- ObjectPropertyAssertion(<http://example.com/family_TBOX.ttl#isMotherOf> <http://example.org/data/PrinceMichaelOfGreeceAndDenmark> <http://example.org/data/PrincessOlgaOfGreece>)

354_354
- ObjectPropertyAssertion(<http://example.com/family_TBOX.ttl#hasMother> <http://example.org/data/Wilhelmina> <http://example.org/data/King_William_III>)
- ClassAssertion(<http://example.com/family_TBOX.ttl#Man> <http://example.org/data/King_William_III>)
- DisjointClasses(<http://example.com/family_TBOX.ttl#Man> <http://example.com/family_TBOX.ttl#Woman>)
- ObjectPropertyRange(<http://example.com/family_TBOX.ttl#hasMother> <http://example.com/family_TBOX.ttl#Woman>)

364_364
- ClassAssertion(<http://example.com/family_TBOX.ttl#Man> <http://example.org/data/Wilhelm_II_German_Emperor>)
- DisjointClasses(<http://example.com/family_TBOX.ttl#Man> <http://example.com/family_TBOX.ttl#Woman>)
- ObjectPropertyAssertion(<http://example.com/family_TBOX.ttl#hasSister> <http://example.org/data/Princess_Sophie_of_Prussia> <http://example.org/data/Wilhelm_II_German_Emperor>)
- ObjectPropertyRange(<http://example.com/family_TBOX.ttl#hasSister> <http://example.com/family_TBOX.ttl#Woman>)

372_372
- SubObjectPropertyOf(<http://example.com/family_TBOX.ttl#hasMother> <http://example.com/family_TBOX.ttl#hasParent>)
- ClassAssertion(<http://example.com/family_TBOX.ttl#Woman> <http://example.org/data/Friederike>)
- ObjectPropertyAssertion(<http://example.com/family_TBOX.ttl#hasMother> <http://example.org/data/GeorgeWilliamOfHanover> <http://example.org/data/SophieOfGreeceAndDenmark>)
- DLSafeRule(Annotation(<http://swrl.stanford.edu/ontologies/3.3/swrla.owl#isRuleEnabled> "true"^^xsd:boolean) Annotation(rdfs:comment "") Annotation(rdfs:label "infer hasSister")  Body(ClassAtom(<http://example.com/family_TBOX.ttl#Woman> Variable(<http://example.com/family_TBOX.ttl#y>)) ObjectPropertyAtom(<http://example.com/family_TBOX.ttl#isSiblingOf> Variable(<http://example.com/family_TBOX.ttl#x>) Variable(<http://example.com/family_TBOX.ttl#y>))) Head(ObjectPropertyAtom(<http://example.com/family_TBOX.ttl#hasSister> Variable(<http://example.com/family_TBOX.ttl#x>) Variable(<http://example.com/family_TBOX.ttl#y>))) )
- ObjectPropertyAssertion(<http://example.com/family_TBOX.ttl#hasDaughter> <http://example.org/data/GeorgeWilliamOfHanover> <http://example.org/data/Friederike>)
- ObjectPropertyAssertion(<http://example.com/family_TBOX.ttl#hasMother> <http://example.org/data/Friederike> <http://example.org/data/SophieOfGreeceAndDenmark>)
- DisjointObjectProperties(<http://example.com/family_TBOX.ttl#hasSister> <http://example.com/family_TBOX.ttl#isParentOf> )
- SubObjectPropertyOf(ObjectPropertyChain( <http://example.com/family_TBOX.ttl#hasParent> <http://example.com/family_TBOX.ttl#isParentOf> ) <http://example.com/family_TBOX.ttl#isSiblingOf>)
- SubObjectPropertyOf(<http://example.com/family_TBOX.ttl#hasDaughter> <http://example.com/family_TBOX.ttl#isParentOf>)
- InverseObjectProperties(<http://example.com/family_TBOX.ttl#hasParent> <http://example.com/family_TBOX.ttl#isParentOf>)

420_420
- ObjectPropertyRange(<http://example.com/family_TBOX.ttl#hasFather> <http://example.com/family_TBOX.ttl#Man>)
- SubObjectPropertyOf(<http://example.com/family_TBOX.ttl#hasFather> <http://example.com/family_TBOX.ttl#hasParent>)
- ObjectPropertyAssertion(<http://example.com/family_TBOX.ttl#hasFather> <http://example.org/data/Georg_Donatus_Hereditary_Grand_Duke_of_Hesse> <http://example.org/data/Louis_Prince_of_Hesse_and_by_Rhine>)
- EquivalentObjectProperties(<http://example.com/family_TBOX.ttl#hasParent> <http://example.com/family_TBOX.ttl#isChildOf> )
- DisjointObjectProperties(<http://example.com/family_TBOX.ttl#hasBrother> <http://example.com/family_TBOX.ttl#isChildOf> )
- ObjectPropertyAssertion(<http://example.com/family_TBOX.ttl#isSiblingOf> <http://example.org/data/Georg_Donatus_Hereditary_Grand_Duke_of_Hesse> <http://example.org/data/Louis_Prince_of_Hesse_and_by_Rhine>)
- DLSafeRule(Annotation(<http://swrl.stanford.edu/ontologies/3.3/swrla.owl#isRuleEnabled> "true"^^xsd:boolean) Annotation(rdfs:comment "") Annotation(rdfs:label "infer hasBrother")  Body(ClassAtom(<http://example.com/family_TBOX.ttl#Man> Variable(<http://example.com/family_TBOX.ttl#y>)) ObjectPropertyAtom(<http://example.com/family_TBOX.ttl#isSiblingOf> Variable(<http://example.com/family_TBOX.ttl#x>) Variable(<http://example.com/family_TBOX.ttl#y>))) Head(ObjectPropertyAtom(<http://example.com/family_TBOX.ttl#hasBrother> Variable(<http://example.com/family_TBOX.ttl#x>) Variable(<http://example.com/family_TBOX.ttl#y>))) )

440_440
- ObjectPropertyRange(<http://example.com/family_TBOX.ttl#hasFather> <http://example.com/family_TBOX.ttl#Man>)
- SubObjectPropertyOf(<http://example.com/family_TBOX.ttl#hasMother> <http://example.com/family_TBOX.ttl#hasParent>)
- SubObjectPropertyOf(<http://example.com/family_TBOX.ttl#hasFather> <http://example.com/family_TBOX.ttl#hasParent>)
- ObjectPropertyAssertion(<http://example.com/family_TBOX.ttl#hasMother> <http://example.org/data/Charles_Hepburn-Stuart-Forbes-Trefusis_20th_Baron_Clinton> <http://example.org/data/Harriet_Williamina_Hepburn-Forbes>)
- ObjectPropertyAssertion(<http://example.com/family_TBOX.ttl#hasFather> <http://example.org/data/Charles_Hepburn-Stuart-Forbes-Trefusis_21st_Baron_Clinton> <http://example.org/data/Charles_Hepburn-Stuart-Forbes-Trefusis_20th_Baron_Clinton>)
- ObjectPropertyAssertion(<http://example.com/family_TBOX.ttl#hasMother> <http://example.org/data/Charles_Hepburn-Stuart-Forbes-Trefusis_21st_Baron_Clinton> <http://example.org/data/Harriet_Williamina_Hepburn-Forbes>)
- SubObjectPropertyOf(ObjectPropertyChain( <http://example.com/family_TBOX.ttl#hasParent> <http://example.com/family_TBOX.ttl#isParentOf> ) <http://example.com/family_TBOX.ttl#isSiblingOf>)
- InverseObjectProperties(<http://example.com/family_TBOX.ttl#hasParent> <http://example.com/family_TBOX.ttl#isParentOf>)
- DisjointObjectProperties(<http://example.com/family_TBOX.ttl#isBrotherOf> <http://example.com/family_TBOX.ttl#isParentOf> )
- InverseObjectProperties(<http://example.com/family_TBOX.ttl#hasBrother> <http://example.com/family_TBOX.ttl#isBrotherOf>)
- DLSafeRule(Annotation(<http://swrl.stanford.edu/ontologies/3.3/swrla.owl#isRuleEnabled> "true"^^xsd:boolean) Annotation(rdfs:comment "") Annotation(rdfs:label "infer hasBrother")  Body(ClassAtom(<http://example.com/family_TBOX.ttl#Man> Variable(<http://example.com/family_TBOX.ttl#y>)) ObjectPropertyAtom(<http://example.com/family_TBOX.ttl#isSiblingOf> Variable(<http://example.com/family_TBOX.ttl#x>) Variable(<http://example.com/family_TBOX.ttl#y>))) Head(ObjectPropertyAtom(<http://example.com/family_TBOX.ttl#hasBrother> Variable(<http://example.com/family_TBOX.ttl#x>) Variable(<http://example.com/family_TBOX.ttl#y>))) )

455_455
- ObjectPropertyAssertion(<http://example.com/family_TBOX.ttl#hasMother> <http://example.org/data/MariaOlympia> <http://example.org/data/Pavlos>)
- ClassAssertion(<http://example.com/family_TBOX.ttl#Man> <http://example.org/data/Pavlos>)
- DisjointClasses(<http://example.com/family_TBOX.ttl#Man> <http://example.com/family_TBOX.ttl#Woman>)
- ObjectPropertyRange(<http://example.com/family_TBOX.ttl#hasMother> <http://example.com/family_TBOX.ttl#Woman>)

485_485
- SubObjectPropertyOf(<http://example.com/family_TBOX.ttl#hasMother> <http://example.com/family_TBOX.ttl#hasParent>)
- ObjectPropertyAssertion(<http://example.com/family_TBOX.ttl#isFatherOf> <http://example.org/data/Prince_Friso> <http://example.org/data/Countess_Joanna_Zaria_Nicoline_Milou>)
- ObjectPropertyAssertion(<http://example.com/family_TBOX.ttl#isMotherOf> <http://example.org/data/Mabel_Wisse_Smit> <http://example.org/data/Countess_Joanna_Zaria_Nicoline_Milou>)
- SubObjectPropertyOf(<http://example.com/family_TBOX.ttl#isFatherOf> <http://example.com/family_TBOX.ttl#isParentOf>)
- ClassAssertion(<http://example.com/family_TBOX.ttl#Woman> <http://example.org/data/Countess_Joanna_Zaria_Nicoline_Milou>)
- DLSafeRule(Annotation(<http://swrl.stanford.edu/ontologies/3.3/swrla.owl#isRuleEnabled> "true"^^xsd:boolean) Annotation(rdfs:comment "") Annotation(rdfs:label "infer hasSister")  Body(ClassAtom(<http://example.com/family_TBOX.ttl#Woman> Variable(<http://example.com/family_TBOX.ttl#y>)) ObjectPropertyAtom(<http://example.com/family_TBOX.ttl#isSiblingOf> Variable(<http://example.com/family_TBOX.ttl#x>) Variable(<http://example.com/family_TBOX.ttl#y>))) Head(ObjectPropertyAtom(<http://example.com/family_TBOX.ttl#hasSister> Variable(<http://example.com/family_TBOX.ttl#x>) Variable(<http://example.com/family_TBOX.ttl#y>))) )
- ObjectPropertyAssertion(<http://example.com/family_TBOX.ttl#hasMother> <http://example.org/data/Prince_Friso> <http://example.org/data/Mabel_Wisse_Smit>)
- DisjointObjectProperties(<http://example.com/family_TBOX.ttl#hasSister> <http://example.com/family_TBOX.ttl#isParentOf> )
- SubObjectPropertyOf(ObjectPropertyChain( <http://example.com/family_TBOX.ttl#hasParent> <http://example.com/family_TBOX.ttl#isParentOf> ) <http://example.com/family_TBOX.ttl#isSiblingOf>)
- SubObjectPropertyOf(<http://example.com/family_TBOX.ttl#isMotherOf> <http://example.com/family_TBOX.ttl#isParentOf>)