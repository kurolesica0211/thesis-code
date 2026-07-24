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
  AssignClass (93694034-4674-488c-802d-bccc092bffab)
 Call ID: 93694034-4674-488c-802d-bccc092bffab
  Args:
    source: Maria_di_Grazia
    type: :Woman
  AssignClass (6928523e-def8-493f-be13-7a892404c506)
 Call ID: 6928523e-def8-493f-be13-7a892404c506
  Args:
    source: Maria_di_Grazia
    type: :Person
  AddLiteral (8d46b6f3-b25a-476a-8289-02164b84ead1)
 Call ID: 8d46b6f3-b25a-476a-8289-02164b84ead1
  Args:
    source: Maria_di_Grazia
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1878
  AddLiteral (16a101c5-c7c5-450e-8b75-902a4de73a60)
 Call ID: 16a101c5-c7c5-450e-8b75-902a4de73a60
  Args:
    literal_value: 1973
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Maria_di_Grazia
  AddLiteral (15657c0a-ac5b-45a8-aa47-8526d177d16f)
 Call ID: 15657c0a-ac5b-45a8-aa47-8526d177d16f
  Args:
    source: Maria_di_Grazia
    relation: :alsoKnownAs
    literal_type: xsd:string
    literal_value: Maria Pia
  AssignClass (8bfe2d4d-e6f6-4db2-9d1f-2e2936f09850)
 Call ID: 8bfe2d4d-e6f6-4db2-9d1f-2e2936f09850
  Args:
    source: Alfonso_Count_of_Caserta
    type: :Man
  AssignClass (1959b307-9417-413d-8150-dd76182659ea)
 Call ID: 1959b307-9417-413d-8150-dd76182659ea
  Args:
    type: :Person
    source: Alfonso_Count_of_Caserta
  AssignClass (d4a13e41-f3d8-4720-b058-f9c076d0c50d)
 Call ID: d4a13e41-f3d8-4720-b058-f9c076d0c50d
  Args:
    source: Alfonso_Count_of_Caserta
    type: :Ancestor
  AssignClass (be016f08-4947-4912-b902-828610cbf3e9)
 Call ID: be016f08-4947-4912-b902-828610cbf3e9
  Args:
    type: :Woman
    source: Antonietta_of_Bourbon-Two_Sicilies
  AssignClass (3005fa56-17ca-4b4d-9a18-8d3d88f057f5)
 Call ID: 3005fa56-17ca-4b4d-9a18-8d3d88f057f5
  Args:
    type: :Person
    source: Antonietta_of_Bourbon-Two_Sicilies
  AssignClass (b329dc08-c882-4b75-8bb6-68b1dadc9903)
 Call ID: b329dc08-c882-4b75-8bb6-68b1dadc9903
  Args:
    source: Antonietta_of_Bourbon-Two_Sicilies
    type: :Ancestor
  AddTriple (49dcce42-03df-41f0-827c-b6a75ed06b34)
 Call ID: 49dcce42-03df-41f0-827c-b6a75ed06b34
  Args:
    source: Maria_di_Grazia
    target: Alfonso_Count_of_Caserta
    relation: :hasFather
  AddTriple (449656a4-95fa-4526-8de6-53ed3e55b337)
 Call ID: 449656a4-95fa-4526-8de6-53ed3e55b337
  Args:
    target: Antonietta_of_Bourbon-Two_Sicilies
    source: Maria_di_Grazia
    relation: :hasMother
  AssignClass (bbded636-77f3-4e64-9d5d-e94bce4e73ed)
 Call ID: bbded636-77f3-4e64-9d5d-e94bce4e73ed
  Args:
    source: Ferdinand_II_of_the_Two_Sicilies
    type: :Man
  AssignClass (a16e0bea-c604-41fc-bdba-8270565570d0)
 Call ID: a16e0bea-c604-41fc-bdba-8270565570d0
  Args:
    type: :Person
    source: Ferdinand_II_of_the_Two_Sicilies
  AssignClass (7d5d315d-7755-49b1-b840-58eb6eccf727)
 Call ID: 7d5d315d-7755-49b1-b840-58eb6eccf727
  Args:
    type: :Ancestor
    source: Ferdinand_II_of_the_Two_Sicilies
  AddTriple (254aa1cb-fc31-4b95-81bf-39e64f087266)
 Call ID: 254aa1cb-fc31-4b95-81bf-39e64f087266
  Args:
    relation: :hasFather
    target: Ferdinand_II_of_the_Two_Sicilies
    source: Alfonso_Count_of_Caserta
  AssignClass (6a79cae8-f4fb-4096-bfad-b301670d2e03)
 Call ID: 6a79cae8-f4fb-4096-bfad-b301670d2e03
  Args:
    type: :Man
    source: Francis_II_of_the_Two_Sicilies
  AssignClass (cc377ef7-54a6-4abd-9aab-b34d9ca956c3)
 Call ID: cc377ef7-54a6-4abd-9aab-b34d9ca956c3
  Args:
    type: :Person
    source: Francis_II_of_the_Two_Sicilies
  AddTriple (23ae9740-5dfc-4a4c-9b6b-a324af818914)
 Call ID: 23ae9740-5dfc-4a4c-9b6b-a324af818914
  Args:
    source: Alfonso_Count_of_Caserta
    target: Francis_II_of_the_Two_Sicilies
    relation: :hasBrother
  AssignClass (3a646f28-5ec6-4232-afef-d6ac3f993634)
 Call ID: 3a646f28-5ec6-4232-afef-d6ac3f993634
  Args:
    source: Luiz_Maria_of_Orléans-Braganza
    type: :Man
  AssignClass (04e5278c-4289-481f-ba30-ef30c246470e)
 Call ID: 04e5278c-4289-481f-ba30-ef30c246470e
  Args:
    source: Luiz_Maria_of_Orléans-Braganza
    type: :Person
  AddLiteral (dbe28ef9-5549-4220-a16a-d7f3b888fe88)
 Call ID: dbe28ef9-5549-4220-a16a-d7f3b888fe88
  Args:
    source: Maria_di_Grazia
    literal_value: 1908
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AddTriple (8e287763-090c-4ec9-b1a7-7ff119b4388e)
 Call ID: 8e287763-090c-4ec9-b1a7-7ff119b4388e
  Args:
    target: Luiz_Maria_of_Orléans-Braganza
    source: Maria_di_Grazia
    relation: :hasRelation
  AssignClass (d7a6f789-775a-490d-b54a-a764636f398f)
 Call ID: d7a6f789-775a-490d-b54a-a764636f398f
  Args:
    source: Gaston_of_Orléans_Count_of_Eu
    type: :Man
  AssignClass (bc62cef8-bbe3-440f-812a-4b06d8408d6c)
 Call ID: bc62cef8-bbe3-440f-812a-4b06d8408d6c
  Args:
    source: Gaston_of_Orléans_Count_of_Eu
    type: :Person
  AssignClass (ece7884f-8e0c-4b73-93d5-4189a82554be)
 Call ID: ece7884f-8e0c-4b73-93d5-4189a82554be
  Args:
    type: :Woman
    source: Isabel_Princess_Imperial_of_Brazil
  AssignClass (2bea7ece-efc6-48d5-b11e-2f6d74dcaff6)
 Call ID: 2bea7ece-efc6-48d5-b11e-2f6d74dcaff6
  Args:
    source: Isabel_Princess_Imperial_of_Brazil
    type: :Person
  AddTriple (778b23b1-5a05-461b-a509-f9f2ae894953)
 Call ID: 778b23b1-5a05-461b-a509-f9f2ae894953
  Args:
    relation: :hasFather
    source: Luiz_Maria_of_Orléans-Braganza
    target: Gaston_of_Orléans_Count_of_Eu
  AddTriple (0b2f2b44-5913-4f7d-a4fe-add5867a41f6)
 Call ID: 0b2f2b44-5913-4f7d-a4fe-add5867a41f6
  Args:
    relation: :hasMother
    source: Luiz_Maria_of_Orléans-Braganza
    target: Isabel_Princess_Imperial_of_Brazil
  AddLiteral (4873b6a3-ad46-4b14-85fd-fb15353bc2ee)
 Call ID: 4873b6a3-ad46-4b14-85fd-fb15353bc2ee
  Args:
    literal_value: 1920
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Luiz_Maria_of_Orléans-Braganza
  Finish (7e0671ec-f855-4b32-9631-3371f1575dd1)
 Call ID: 7e0671ec-f855-4b32-9631-3371f1575dd1
  Args: