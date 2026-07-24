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
Princess Maria di Grazia of Bourbon-Two Sicilies (12 August 1878 – 20 June 1973) was a Princess of Bourbon-Two Sicilies by birth as well as Princess Imperial of Brazil and Princess of Orleans-Braganza through her marriage to Prince Luiz of Orléans-Braganza, secondborn son and pretense heir of Isabel, Princess Imperial of Brazil.
Early life and family

Princess Maria was born at their parents' Villa Maria Teresa in Cannes, where her family had been exiled since the 1861 due to the Italian Unification.
She was the sixth child and third daughter of Prince Alfonso, Count of Caserta and his wife Princess Antonietta of Bourbon-Two Sicilies.
She was usually called “Maria Pia”.
Her father, the third son of King Ferdinand II of the Two Sicilies, became Head of the Royal House of the Two Sicilies with the death of his elder brother, King Francis II, in 1894.
Maria di Grazia was baptized and had Robert I, Duke of Parma, and his first wife, Princess Maria Pia of the Two Sicilies, as godparents.
Maria di Grazia and her sisters were educated at the College of the Sacred Heart of Aix-Provence, an institution run by nuns near Cannes.
There, Maria di Grazia spent her childhood and, after finishing her studies, her youth.
In one of the visits of the Emperor Pedro II of Brazil to Cannes, he visited the Villa Maria Teresa.
The Count of Caserta gathered all his children to present them to the monarch, and Maria di Grazia, at the age of ten, had to play "Turkish March" by Mozart, on the piano.
Upon turning 18, Maria di Grazia was taken with her sisters to be presented to the court of Emperor Franz Joseph I of Austria.
After Austria, the princesses were taken to Munich, where they were given a gala lunch by Luitpold, Prince Regent of Bavaria.
Marriage and issue

Princess Maria di Grazia met her future fiancé when they were still young, when Luiz eventually arrived in Europe due to the exile imposed by the proclamation of the republic in Brazil in 1889.
They later reconnected in 1903 when Prince Luiz, then serving in the Austrian Army, was visiting several relatives in France.
On 4 November 1908 Princess Maria di Grazia married Prince Luiz Maria of Orléans-Braganza, son of Prince Gaston of Orléans, Count of Eu and Isabel, Princess Imperial of Brazil, in Cannes.
Later life

Prince Luiz died in 1920 leaving Maria a widow for the remainder of her life.
In 1922, Maria accompanied the Brazilian Imperial Family to Brazil for the country's centennial celebrations of its independence.
During the course of the trip, the Count of Eu died while recumbent upon her shoulder.
After that, Princess Maria preferred to live with her children in France, where they could have a better education.
}} Media related to Princess Maria di Grazia of the Two Sicilies at Wikimedia Commons



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
  AssignClass (8aa73f67-de6b-4b89-b85f-e30b1ffb3e5f)
 Call ID: 8aa73f67-de6b-4b89-b85f-e30b1ffb3e5f
  Args:
    type: :Woman
    source: :Maria_di_Grazia
  AssignClass (c4227eb9-f094-4e6e-9c24-560059c0ca5a)
 Call ID: c4227eb9-f094-4e6e-9c24-560059c0ca5a
  Args:
    type: :Person
    source: :Maria_di_Grazia
  AddLiteral (938eda7e-d6f6-4411-b36c-e9a31206e382)
 Call ID: 938eda7e-d6f6-4411-b36c-e9a31206e382
  Args:
    relation: :hasBirthYear
    literal_value: 1878
    literal_type: xsd:integer
    source: :Maria_di_Grazia
  AddLiteral (bad8aba2-02b6-4c39-b19a-16ffa970dcf9)
 Call ID: bad8aba2-02b6-4c39-b19a-16ffa970dcf9
  Args:
    source: :Maria_di_Grazia
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1973
  AddLiteral (d123c463-4612-4101-aaf3-0da1a3b972e6)
 Call ID: d123c463-4612-4101-aaf3-0da1a3b972e6
  Args:
    relation: :knownAs
    literal_value: Maria Pia
    literal_type: xsd:string
    source: :Maria_di_Grazia
  AssignClass (567a2560-fbc9-457e-b8c0-daf4eb224220)
 Call ID: 567a2560-fbc9-457e-b8c0-daf4eb224220
  Args:
    type: :Man
    source: :Alfonso_Count_of_Caserta
  AssignClass (1073a70b-34f0-42d7-bd9e-fc87eff2e3ca)
 Call ID: 1073a70b-34f0-42d7-bd9e-fc87eff2e3ca
  Args:
    type: :Person
    source: :Alfonso_Count_of_Caserta
  AssignClass (67da16a8-3269-459c-a549-518018c96cca)
 Call ID: 67da16a8-3269-459c-a549-518018c96cca
  Args:
    type: :Woman
    source: :Antonietta_of_Bourbon-Two_Sicilies
  AssignClass (b7728b2d-c06f-4128-838b-0936a549246a)
 Call ID: b7728b2d-c06f-4128-838b-0936a549246a
  Args:
    type: :Person
    source: :Antonietta_of_Bourbon-Two_Sicilies
  AddTriple (ef0d08b8-5f3c-4228-b325-d16771d3c649)
 Call ID: ef0d08b8-5f3c-4228-b325-d16771d3c649
  Args:
    source: :Maria_di_Grazia
    target: :Alfonso_Count_of_Caserta
    relation: :hasFather
  AddTriple (36ea70c4-bcdf-4860-851a-50bd7a9dc4e4)
 Call ID: 36ea70c4-bcdf-4860-851a-50bd7a9dc4e4
  Args:
    relation: :hasMother
    target: :Antonietta_of_Bourbon-Two_Sicilies
    source: :Maria_di_Grazia
  AssignClass (c8d05329-ee55-4d17-9cba-effa38f08b8a)
 Call ID: c8d05329-ee55-4d17-9cba-effa38f08b8a
  Args:
    type: :Man
    source: :Luiz_of_Orleans-Braganza
  AssignClass (1b571006-ecfd-4f18-8dd7-536ddf7795b5)
 Call ID: 1b571006-ecfd-4f18-8dd7-536ddf7795b5
  Args:
    type: :Person
    source: :Luiz_of_Orleans-Braganza
  AddLiteral (d9c80433-7515-45d2-96ce-6366ff345a93)
 Call ID: d9c80433-7515-45d2-96ce-6366ff345a93
  Args:
    source: :Maria_di_Grazia
    literal_type: xsd:integer
    literal_value: 1908
    relation: :hasMarriageYear
  AddTriple (d18cb79c-20d7-4562-9d28-8c8172e32f86)
 Call ID: d18cb79c-20d7-4562-9d28-8c8172e32f86
  Args:
    source: :Maria_di_Grazia
    target: :Luiz_of_Orleans-Braganza
    relation: :hasRelation
  AssignClass (a2a54d3b-8f4d-403a-8b87-0a50432f1ecd)
 Call ID: a2a54d3b-8f4d-403a-8b87-0a50432f1ecd
  Args:
    type: :Man
    source: :Gaston_of_Orleans_Count_of_Eu
  AssignClass (98d3471d-16a5-45e0-82e9-5250f15655c9)
 Call ID: 98d3471d-16a5-45e0-82e9-5250f15655c9
  Args:
    type: :Person
    source: :Gaston_of_Orleans_Count_of_Eu
  AssignClass (9323c1b4-9e4f-43f1-a431-5c9061f1abd3)
 Call ID: 9323c1b4-9e4f-43f1-a431-5c9061f1abd3
  Args:
    type: :Woman
    source: :Isabel_Princess_Imperial_of_Brazil
  AssignClass (34ecc385-556c-4b03-acab-99a59e2a39ef)
 Call ID: 34ecc385-556c-4b03-acab-99a59e2a39ef
  Args:
    type: :Person
    source: :Isabel_Princess_Imperial_of_Brazil
  AddTriple (2edb4bc4-a74e-4ed3-8b7c-4f3f7c1decae)
 Call ID: 2edb4bc4-a74e-4ed3-8b7c-4f3f7c1decae
  Args:
    source: :Luiz_of_Orleans-Braganza
    target: :Gaston_of_Orleans_Count_of_Eu
    relation: :hasFather
  AddTriple (4ffb754e-1451-4180-845b-48014f5d8b0f)
 Call ID: 4ffb754e-1451-4180-845b-48014f5d8b0f
  Args:
    target: :Isabel_Princess_Imperial_of_Brazil
    relation: :hasMother
    source: :Luiz_of_Orleans-Braganza
  AssignClass (bde7dc97-9576-4f5e-a0d1-1fad1dcf9f4f)
 Call ID: bde7dc97-9576-4f5e-a0d1-1fad1dcf9f4f
  Args:
    type: :Man
    source: :Ferdinand_II_of_the_Two_Sicilies
  AssignClass (154230e0-e211-4475-a040-a0349afc9dff)
 Call ID: 154230e0-e211-4475-a040-a0349afc9dff
  Args:
    type: :Person
    source: :Ferdinand_II_of_the_Two_Sicilies
  AddTriple (31684a40-4066-4d4d-9bc9-4e8493f6e3c0)
 Call ID: 31684a40-4066-4d4d-9bc9-4e8493f6e3c0
  Args:
    relation: :hasFather
    target: :Ferdinand_II_of_the_Two_Sicilies
    source: :Alfonso_Count_of_Caserta
  AssignClass (e6d5f5db-4a42-4cec-816c-7d5ff3b066c5)
 Call ID: e6d5f5db-4a42-4cec-816c-7d5ff3b066c5
  Args:
    type: :Man
    source: :Francis_II_of_the_Two_Sicilies
  AssignClass (ad038bab-8367-4d55-b809-7f6b6da5882d)
 Call ID: ad038bab-8367-4d55-b809-7f6b6da5882d
  Args:
    type: :Person
    source: :Francis_II_of_the_Two_Sicilies
  AddTriple (52c69cb3-5812-40d8-b822-52bb1ebd87a1)
 Call ID: 52c69cb3-5812-40d8-b822-52bb1ebd87a1
  Args:
    relation: :isBrotherOf
    target: :Alfonso_Count_of_Caserta
    source: :Francis_II_of_the_Two_Sicilies
  AssignClass (4887dd7a-3012-4ba5-a835-5187f8f897ea)
 Call ID: 4887dd7a-3012-4ba5-a835-5187f8f897ea
  Args:
    type: :Man
    source: :Robert_I_Duke_of_Parma
  AssignClass (e6146cf7-4c95-4242-809f-89bf05488647)
 Call ID: e6146cf7-4c95-4242-809f-89bf05488647
  Args:
    type: :Person
    source: :Robert_I_Duke_of_Parma
  AssignClass (d51e1d20-f7e7-4dbb-ac40-21cdc5bd0468)
 Call ID: d51e1d20-f7e7-4dbb-ac40-21cdc5bd0468
  Args:
    type: :Woman
    source: :Maria_Pia_of_the_Two_Sicilies
  AssignClass (ac1ec35f-ce62-4156-bc15-16e13f5726c5)
 Call ID: ac1ec35f-ce62-4156-bc15-16e13f5726c5
  Args:
    type: :Person
    source: :Maria_Pia_of_the_Two_Sicilies
  Finish (937f1d03-46d4-4819-80f3-4aed3afc68c8)
 Call ID: 937f1d03-46d4-4819-80f3-4aed3afc68c8
  Args: