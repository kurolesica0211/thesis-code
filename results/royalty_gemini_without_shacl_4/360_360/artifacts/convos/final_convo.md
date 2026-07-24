================================ System Message ================================

### Role
You are an expert Knowledge Graph Engineer. Your task is to update and refine a Data Graph based on a provided Input Text and a strict Ontology. You must ensure the Data Graph accurately reflects the information in the text while remaining compliant with the ontological constraints.

### Inputs
1. **Ontology**: Allowed classes and properties.
2. **Input Text**: The ONLY source of truth.
3. **Current Data Graph**: The starting state.

### Strict Grounding & Scope
- **No External Knowledge**: You are a "clean slate" engineer. Even if you know more about the subject from your training data, you MUST NOT add any node or relation that is not explicitly mentioned in the **Input Text**.
- **No Hypothetical Nodes**: Do not create placeholder nodes or sequences (e.g., Marriage1, Marriage2) to represent "patterns" mentioned in the text. Only create nodes for specific instances described.
- **Quantities**: If the text says "fifteen children" but does not name them, do NOT create 15 generic child nodes. Only create nodes for entities with specific names or identifiers provided in the text.

### Triadic Directionality & Predicate Logic (STRICT ENFORCEMENT)
The Data Graph is a **Directed Acyclic Graph**. Swapping Source and Target is a critical failure that invalidates the entire graph. You MUST follow the **Flow of Action**.

#### 1. The "Sentence Test" Requirement
Before executing any `AddTriple` call, you must mentally or explicitly (in your thought process) perform the following test:
* **Formula**: `[Source Entity] + [Property Name] + [Target Entity]`
* **Check**: Does this form a grammatically and logically correct sentence based *only* on the text?
* **Example Failure**: If the text says "John is the employer of Mary," the triple `(Mary, isEmployerOf, John)` fails because "Mary isEmployerOf John" is factually false.

#### 2. Identifying the Anchor (Domain vs. Range)
* **The Source**: The "Origin" or "Owner." If the property is a verb, the Source is the one performing it. Source is always to the left of a relation.
* **The Target**: The "Destination" or "Attribute." If the property is a verb, the Target is the one being acted upon. Target is always to the right of a relation.

#### 3. Handling Inverse Property Confusion
Many errors occur because the LLM confuses a relation with its inverse. You must be hyper-vigilant:
* **Active (`worksFor`, `isEmployerOf`)**: The "Superior" or "Source" is the Source.
* **Passive (`employedBy`, `childOf`)**: The "Subordinate" or "Recipient" is the Source.
* **Partitive (`hasPart`, `contains`)**: The "Container/Whole" is the Source.
* **Membership (`isPartOf`, `memberOf`)**: The "Component/Part" is the Source.

#### 4. Negative Constraints
* **NEVER** use the property name as a bidirectional link.
* **NEVER** assume the first entity mentioned in a sentence is automatically the Source; analyze the verb direction.

#### 5. Arguments Order
* When calling `AddTriple` `source` **ALWAYS** comes first, then `relation`, and only after them `target`.

> **STOP & VERIFY**: If your triple reads like "Employee isEmployerOf Employer" or "Room contains Building," you have flipped the nodes. **STOP and swap them before calling the tool.**


### Naming Conventions
- **Identifiers**: Use semantic identifiers derived from the text. 
- **Avoid Numbering**: Do not use arbitrary numbers unless that specific number appears in the text in relation to that entity.
- **Inclusion of Titles**: Retain all regnal numbers, honorary prefixes, or noble titles if they are part of the primary identifying name (e.g., "Crown Prince [Name]" or "[Name] II").
- **Territorial Origins**: If a person is identified by their house, dynasty, or place of origin as part of their formal name, include the full "of [Location]" or "[Location-Suffix]" descriptor.
- **Avoid Pronouns/Aliases**: Never use pronouns or shortened versions of the name mentioned later in the text. Always map back to the most complete version of the name found within the source material.

### Instructions & Workflow
1. **Analyze**: Identify specific entities and relations in the text.
2. **Edit**: Use tools to modify the graph.
   - Every node MUST have a class assignment (`AssignClass`).
   - Ground every edit in text evidence.
3. **Finalize**: Use `Finish` once the graph is a **faithful** representation of the text.

### Tool Usage Constraints
- **AssignClass / UnassignClass**: For `rdf:type` only.
- **AddTriple / RemoveTriple**: For properties only.
- **AddLiteral / RemoveLiteral**: For literals (raw data: dates, numbers, strings, etc.) only.
- **Finish**: Once you are finished, use this tool.
- **Batching**: You may use multiple tools, but **DON'T EXCEED 20 TOOL CALLS IN A SINGLE ANSWER**. Focus on quality and grounding over quantity.

================================ Human Message =================================

Please update the Knowledge Graph based on the provided data.

### Input Text:
Prince Joachim Franz Humbert of Prussia (17 December 1890 – 18 July 1920) was the youngest son and sixth child of Wilhelm II, German Emperor, by his first wife, Augusta Victoria of Schleswig-Holstein.
Prince Joachim was educated as an officer and participated in the First World War.
Early life

Birth and family

Prince Joachim was born on 17 December 1890, two years after his father had become the German Emperor, at the Berlin Palace in central Berlin.
He was the sixth and youngest son of Emperor Wilhelm II, and his first wife, Princess Augusta Victoria of Schleswig-Holstein.
Education

Prince Joachim spent his childhood with his siblings at the New Palace in Potsdam, and his school days at the Prinzenhaus in Plön, in his mother's ancestral Schleswig-Holstein, as his brothers had been before him.
Marriage

On 11 March 1916 in Berlin, Joachim married Princess Marie-Auguste of Anhalt (10 June 1898 – 22 May 1983), the daughter of Eduard, Duke of Anhalt and his wife Princess Luise of Saxe-Altenburg (daughter of Prince Moritz of Saxe-Altenburg).
He and Marie-Auguste had been engaged since 14 October of the previous year.
The wedding was celebrated at Bellevue Palace, and was attended by Joachim's father and mother, the Duke and Duchess of Anhalt, as well as other relatives.
The couple had one son, Prince Karl Franz Josef Wilhelm Friedrich Eduard Paul (15 December 1916 in Potsdam – 22 January 1975 in Arica, Chile).
Their grandson, Prince Franz Wilhelm, married Maria Vladimirovna of Russia, a claimant to the Imperial Russian throne.
Candidate for thrones

Ireland

During the Easter Rising in Dublin in 1916, some republican leaders, including Patrick Pearse and Joseph Plunkett, contemplated giving the throne of an independent Ireland to Prince Joachim.
Pearse and Plunkett thought that if the rising were successful and Germany won the First World War, an independent Ireland would be a monarchy with a German prince as king, like Romania and Bulgaria before it.
The fact that Joachim did not speak English was also considered an advantage, as he might be more disposed to learning and promoting the use of the Irish language.
He would naturally turn to those who were more Irish and Gaelic, as to his friends, for the non-nationalist element in our country had shown themselves to be so bitterly anti-German.
For the first generation or so it would be an advantage, in view of our natural weakness, to have a ruler who linked us with a dominant European power, and thereafter, when we were better prepared to stand alone, or when it might be undesirable that our ruler should turn by personal choice to one power rather than be guided by what was most natural and beneficial for our country, the ruler of that time would have become completely Irish."

Ernest Blythe recalled that in January 1915 he heard Plunkett and Thomas MacDonagh express support for the idea at an Irish Volunteers meeting.
Georgia

After Georgia's declaration of independence following the Russian Revolution of 1917, Joachim was briefly considered by the German representative Count Friedrich Werner von der Schulenburg and Georgian royalists as a candidate for the Georgian throne.
The Germans presented various proposals to incorporate Lithuania into the German Empire, particularly Prussia.
One such proposal offered the crown of Lithuania to Joachim.
On 4 June 1918, they voted to offer the Lithuanian throne to the German noble Wilhelm Karl, Duke of Urach.
Divorce and death

Following the German Revolution in November 1918, the Emperor was forced to abdicate, thus depriving Joachim of his titles, position and prospects for heading any newly established monarchies in Europe.
On 31 May 1918, Joachim was examined by the psychiatrist Robert Gaupp, who submitted a report concluding that he "was incurably ill, both mentally and physically ... was extremely easily emotionally and sexually aroused", and "was inclined to 'violent, uncontrollably exploding outbursts of anger in which all self-control  lost'".
The relationship between Joachim and his wife had already started to deteriorate.
According to one report, Marie-Auguste had previously abandoned her husband and child to run away with another man, had been forcibly brought back home on the orders of the Kaiser, but had filed for divorce as soon as the war ended, when she saw that her husband's family were at their lowest ebb.
According to Hans von Gontard, who served as the Kaiser's Hofmarschall in exile, Joachim was "quite out of control and had beaten his wife".
Following the divorce, Joachim shot himself in Potsdam on 18 July 1920.
His own brother Prince Eitel Friedrich of Prussia commented that he suffered from "a fit of excessive dementia".
Kaiser Wilhelm's reaction to the news of his son's suicide was one of fury, commenting that he was outraged "that the oaf should have done this, too, to us and especially to his mother!"
She desperately wanted to believe that his death had been accidental but she knew better.


Children and grandchildren

The only issue of the marriage of Prince Joachim and Princess Marie-Auguste was their son, Prince Karl Franz Josef Wilhelm Friedrich Eduard of Prussia (15 December 1916 – 22 January 1975).
On 5 October 1940, Prince Karl married Princess Henriette Hermine Wanda Ida Luise von Schönaich-Carolath (25 November 1918 –
They were the parents of three children:


After the divorce, Prince Karl married, morganatically, Luise Dora Hartmann (5 September 1909 – 23 April 1961) on 9 November 1946.
Prince Karl's last marriage was to Eva Maria Herrera y Valdeavellano (10 June 1922 – 6 March 1987) on 20 July 1959 in Lima, Peru.
They were married until Prince Karl's death and had two daughters;


Regimental Commissions

Honours

Prince Joachim received the following orders and decorations:
Ancestry

Portrayal in fiction

Prince Joachim was played by American actor Jesse Plemons and portrayed as the main antagonist in the 2021 Disney fantasy adventure film Jungle Cruise.



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://www.w3.org/2003/11/swrl#> .
@prefix ns2: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

: a owl:Ontology ;
    dcterms:source <http://www.co-ode.org/roberts/family-tree.owl> .

:alsoKnownAs a owl:AnnotationProperty .

:formerlyKnownAs a owl:AnnotationProperty .

:hasBirthYear a rdfs:Datatype,
        owl:AnnotationProperty .

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

:isAuntOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isSisterOf :isParentOf ) .

:isUncleOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isBrotherOf :isParentOf ) .

:knownAs a owl:AnnotationProperty .

dcterms:source a owl:AnnotationProperty .

ns2:isRuleEnabled a owl:AnnotationProperty .

:hasBrother a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isBrotherOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasDaughter a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isDaughterOf .

:hasFather a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Man ;
    rdfs:subPropertyOf :hasParent ;
    owl:inverseOf :isFatherOf .

:hasMother a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Woman ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf ;
    owl:inverseOf :isMotherOf .

:hasSister a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isSisterOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasSon a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isSonOf .

:isBloodrelationOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty .

:isDaughterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:isFatherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isMotherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isSonOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:DomainEntity a owl:Class .

:Female a owl:Class ;
    rdfs:subClassOf :Sex ;
    owl:disjointWith :Male .

:hasAncestor a owl:ObjectProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty ;
    owl:inverseOf :isAncestorOf .

:isBrotherOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:Male a owl:Class ;
    rdfs:subClassOf :Sex .

:hasRelation a owl:ObjectProperty,
        owl:SymmetricProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person .

:hasSex a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Sex .

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:x a ns1:Variable .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:y a ns1:Variable .

:Ancestor a owl:Class ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :isAncestorOf ;
                        owl:someValuesFrom :Person ] ) ] .

:Person a owl:Class ;
    rdfs:subClassOf [ a owl:Restriction ;
            owl:onProperty :hasFather ;
            owl:someValuesFrom :Man ],
        [ a owl:Restriction ;
            owl:onProperty :hasMother ;
            owl:someValuesFrom :Woman ],
        [ a owl:Restriction ;
            owl:onProperty :hasSex ;
            owl:someValuesFrom :Sex ],
        [ a owl:Restriction ;
            owl:maxQualifiedCardinality "2"^^xsd:nonNegativeInteger ;
            owl:onClass :Person ;
            owl:onProperty :hasParent ],
        :DomainEntity ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Man :Woman ) ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSon" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasBrother" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSister" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (e4f7a6e3-6a8a-40c5-85dc-e023f1e53ce8)
 Call ID: e4f7a6e3-6a8a-40c5-85dc-e023f1e53ce8
  Args:
    type: :Man
    source: Prince_Joachim_of_Prussia
  AssignClass (660b4ec3-6c7e-4cc7-863c-a7bca2e41a7c)
 Call ID: 660b4ec3-6c7e-4cc7-863c-a7bca2e41a7c
  Args:
    type: :Man
    source: Wilhelm_II
  AssignClass (3356d901-1b73-41a8-9c23-1e6f55ac59b9)
 Call ID: 3356d901-1b73-41a8-9c23-1e6f55ac59b9
  Args:
    type: :Woman
    source: Augusta_Victoria_of_Schleswig-Holstein
  AddLiteral (13414878-c442-4d78-b1ce-9131728bd81c)
 Call ID: 13414878-c442-4d78-b1ce-9131728bd81c
  Args:
    literal_value: 1890
    literal_type: xsd:nonNegativeInteger
    relation: :hasBirthYear
    source: Prince_Joachim_of_Prussia
  AddLiteral (bc577594-f872-46c8-9fcc-7323b29a74ee)
 Call ID: bc577594-f872-46c8-9fcc-7323b29a74ee
  Args:
    source: Prince_Joachim_of_Prussia
    literal_value: 1920
    literal_type: xsd:nonNegativeInteger
    relation: :hasDeathYear
  AddTriple (98899435-ecb3-4868-8ede-a72ed6146a5e)
 Call ID: 98899435-ecb3-4868-8ede-a72ed6146a5e
  Args:
    target: Wilhelm_II
    relation: :hasFather
    source: Prince_Joachim_of_Prussia
  AddTriple (aef8f016-2638-4123-9f5a-014463a919a7)
 Call ID: aef8f016-2638-4123-9f5a-014463a919a7
  Args:
    target: Augusta_Victoria_of_Schleswig-Holstein
    relation: :hasMother
    source: Prince_Joachim_of_Prussia
  AssignClass (a90434ed-5d34-4f40-a8d4-65e6be27556a)
 Call ID: a90434ed-5d34-4f40-a8d4-65e6be27556a
  Args:
    type: :Woman
    source: Marie-Auguste_of_Anhalt
  AddLiteral (39b7bb87-0737-4779-8a89-26e752d8fa57)
 Call ID: 39b7bb87-0737-4779-8a89-26e752d8fa57
  Args:
    relation: :hasBirthYear
    literal_type: xsd:nonNegativeInteger
    literal_value: 1898
    source: Marie-Auguste_of_Anhalt
  AddLiteral (30251c7d-2f6f-43a1-810f-a3c98d053b28)
 Call ID: 30251c7d-2f6f-43a1-810f-a3c98d053b28
  Args:
    source: Marie-Auguste_of_Anhalt
    literal_value: 1983
    literal_type: xsd:nonNegativeInteger
    relation: :hasDeathYear
  AddLiteral (8dea8269-0399-48bc-9c6e-6c98efda11d0)
 Call ID: 8dea8269-0399-48bc-9c6e-6c98efda11d0
  Args:
    source: Prince_Joachim_of_Prussia
    literal_value: 1916
    literal_type: xsd:nonNegativeInteger
    relation: :hasMarriageYear
  AddTriple (f2aff65e-caae-46e9-8576-33af0a93ce2e)
 Call ID: f2aff65e-caae-46e9-8576-33af0a93ce2e
  Args:
    source: Prince_Joachim_of_Prussia
    target: Marie-Auguste_of_Anhalt
    relation: :hasRelation
  AssignClass (30105ce6-a521-4301-a754-501b8ff3da3a)
 Call ID: 30105ce6-a521-4301-a754-501b8ff3da3a
  Args:
    type: :Man
    source: Karl_Franz_Josef_Wilhelm_Friedrich_Eduard_Paul_of_Prussia
  AddLiteral (4769869d-0cef-4e28-826f-3c2f039f8029)
 Call ID: 4769869d-0cef-4e28-826f-3c2f039f8029
  Args:
    source: Karl_Franz_Josef_Wilhelm_Friedrich_Eduard_Paul_of_Prussia
    literal_type: xsd:nonNegativeInteger
    literal_value: 1916
    relation: :hasBirthYear
  AddLiteral (f9b20db4-ed25-494b-bfe7-a314c6579742)
 Call ID: f9b20db4-ed25-494b-bfe7-a314c6579742
  Args:
    literal_value: 1975
    literal_type: xsd:nonNegativeInteger
    relation: :hasDeathYear
    source: Karl_Franz_Josef_Wilhelm_Friedrich_Eduard_Paul_of_Prussia
  AddTriple (8eef26e6-911f-4c74-9035-151767a1d3f3)
 Call ID: 8eef26e6-911f-4c74-9035-151767a1d3f3
  Args:
    relation: :hasFather
    target: Prince_Joachim_of_Prussia
    source: Karl_Franz_Josef_Wilhelm_Friedrich_Eduard_Paul_of_Prussia
  AddTriple (44ca6131-a093-420a-be13-6484b04ebf88)
 Call ID: 44ca6131-a093-420a-be13-6484b04ebf88
  Args:
    source: Karl_Franz_Josef_Wilhelm_Friedrich_Eduard_Paul_of_Prussia
    relation: :hasMother
    target: Marie-Auguste_of_Anhalt
  AssignClass (75550ac5-5f8a-4a18-ab55-c7f3ec07c3fe)
 Call ID: 75550ac5-5f8a-4a18-ab55-c7f3ec07c3fe
  Args:
    type: :Man
    source: Eduard_Duke_of_Anhalt
  AssignClass (3e4447b4-13ab-4063-9aae-a78b2e9596e9)
 Call ID: 3e4447b4-13ab-4063-9aae-a78b2e9596e9
  Args:
    type: :Woman
    source: Luise_of_Saxe-Altenburg
  AddTriple (bee336e6-db0c-44f4-88c0-f878391ff8bc)
 Call ID: bee336e6-db0c-44f4-88c0-f878391ff8bc
  Args:
    relation: :hasFather
    target: Eduard_Duke_of_Anhalt
    source: Marie-Auguste_of_Anhalt
  AddTriple (ae47a9b5-9602-4bfc-b337-e139ce768ee5)
 Call ID: ae47a9b5-9602-4bfc-b337-e139ce768ee5
  Args:
    relation: :hasMother
    target: Luise_of_Saxe-Altenburg
    source: Marie-Auguste_of_Anhalt
  AssignClass (b1fb81c3-94d3-4335-991f-8d7f963f383d)
 Call ID: b1fb81c3-94d3-4335-991f-8d7f963f383d
  Args:
    type: :Man
    source: Moritz_of_Saxe-Altenburg
  AddTriple (a7425c10-d6cc-4179-9339-185daefe6d65)
 Call ID: a7425c10-d6cc-4179-9339-185daefe6d65
  Args:
    relation: :hasFather
    target: Moritz_of_Saxe-Altenburg
    source: Luise_of_Saxe-Altenburg
  AssignClass (77e38f13-1b94-4aa3-bf6a-9b37d558ea2a)
 Call ID: 77e38f13-1b94-4aa3-bf6a-9b37d558ea2a
  Args:
    type: :Woman
    source: Henriette_Hermine_Wanda_Ida_Luise_von_Schönaich-Carolath
  AddLiteral (3d48744b-f20d-4df9-a007-66293ec7ad5c)
 Call ID: 3d48744b-f20d-4df9-a007-66293ec7ad5c
  Args:
    relation: :hasBirthYear
    literal_type: xsd:nonNegativeInteger
    literal_value: 1918
    source: Henriette_Hermine_Wanda_Ida_Luise_von_Schönaich-Carolath
  AddTriple (c2c1fc04-2359-430b-90f5-5b4b9b98b566)
 Call ID: c2c1fc04-2359-430b-90f5-5b4b9b98b566
  Args:
    target: Henriette_Hermine_Wanda_Ida_Luise_von_Schönaich-Carolath
    relation: :hasRelation
    source: Karl_Franz_Josef_Wilhelm_Friedrich_Eduard_Paul_of_Prussia
  AssignClass (b229844b-b475-45f0-8314-c5a4678ae54a)
 Call ID: b229844b-b475-45f0-8314-c5a4678ae54a
  Args:
    type: :Woman
    source: Luise_Dora_Hartmann
  AddLiteral (7b621656-3a36-4a77-a7ea-18c00d8203a6)
 Call ID: 7b621656-3a36-4a77-a7ea-18c00d8203a6
  Args:
    source: Luise_Dora_Hartmann
    relation: :hasBirthYear
    literal_type: xsd:nonNegativeInteger
    literal_value: 1909
  AddLiteral (3b77087e-b6f5-4221-922e-4dda84d19027)
 Call ID: 3b77087e-b6f5-4221-922e-4dda84d19027
  Args:
    relation: :hasDeathYear
    literal_type: xsd:nonNegativeInteger
    literal_value: 1961
    source: Luise_Dora_Hartmann
  AddTriple (f6f21acc-8001-482d-8160-ca8460724575)
 Call ID: f6f21acc-8001-482d-8160-ca8460724575
  Args:
    source: Karl_Franz_Josef_Wilhelm_Friedrich_Eduard_Paul_of_Prussia
    target: Luise_Dora_Hartmann
    relation: :hasRelation
  AssignClass (27d1c002-febc-4318-9b88-7c339cc3dcc8)
 Call ID: 27d1c002-febc-4318-9b88-7c339cc3dcc8
  Args:
    type: :Woman
    source: Eva_Maria_Herrera_y_Valdeavellano
  AddLiteral (8ff67f4c-7b23-420d-a7e4-b44addd8dc19)
 Call ID: 8ff67f4c-7b23-420d-a7e4-b44addd8dc19
  Args:
    source: Eva_Maria_Herrera_y_Valdeavellano
    relation: :hasBirthYear
    literal_type: xsd:nonNegativeInteger
    literal_value: 1922
  AddLiteral (8dc0d35f-469e-4d39-bdb5-a230035c1f47)
 Call ID: 8dc0d35f-469e-4d39-bdb5-a230035c1f47
  Args:
    literal_value: 1987
    literal_type: xsd:nonNegativeInteger
    relation: :hasDeathYear
    source: Eva_Maria_Herrera_y_Valdeavellano
  AddTriple (d0bed1a7-053e-46d1-9dab-787d9b925e1a)
 Call ID: d0bed1a7-053e-46d1-9dab-787d9b925e1a
  Args:
    source: Karl_Franz_Josef_Wilhelm_Friedrich_Eduard_Paul_of_Prussia
    relation: :hasRelation
    target: Eva_Maria_Herrera_y_Valdeavellano
  Finish (e5ad1e43-cd1d-4e5f-ad7b-e252e634e58b)
 Call ID: e5ad1e43-cd1d-4e5f-ad7b-e252e634e58b
  Args: