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
Princess Christina of the Netherlands (Maria Christina; 18 February 1947 – 16 August 2019) was the youngest of four daughters of Queen Juliana of the Netherlands and Prince Bernhard of Lippe-Biesterfeld.
She taught singing in New York and was a long-term supporter of the Youth Music Foundation in the Netherlands.
Christina died of bone cancer in 2019.
Early life

Princess Christina, who was known as Princess Marijke in her youth, was born on 18 February 1947, at Soestdijk Palace, Baarn, the Netherlands.
Her parents were Crown Princess Juliana, the only child of Queen Wilhelmina of the Netherlands, and Prince Bernhard of Lippe-Biesterfeld.
At the time of her birth, she was fifth in the line to the throne after her mother and three older sisters: Princess Beatrix, Princess Irene and Princess Margriet.
She was baptised on 9 October 1947 and her godparents included Queen Wilhelmina (her maternal grandmother), her eldest sister Princess Beatrix, Sir Winston Churchill (for whom her father stood proxy), her paternal grandmother Princess Armgard of Lippe-Biesterfeld, Prince Felix of Luxembourg, and his niece Princess Anne of Bourbon-Parma.
On 4 September 1948, after a reign of nearly 58 years, Christina's grandmother Queen Wilhelmina (68) abdicated the throne and her mother was inaugurated as Queen of the Kingdom of the Netherlands on 6 September 1948.
Childhood and education

While her mother was pregnant with Christina, she contracted either measles or rubella and as a result, Christina was born nearly blind.
In 1963, she stopped using her first name Maria, from then on referring to herself merely as Christina.
Marriage

While living in New York as Christina van Oranje, the Princess started a relationship with Cuban exile Jorge Guillermo.
Although societal attitudes were changing, because Guillermo was a Catholic, it was still possible that a marriage could cause a public scandal in the Netherlands such as the one that occurred in 1964 when Christina's sister Princess Irene married the Catholic Prince Carlos Hugo of Bourbon-Parma.
Accordingly, Princess Christina, at that time ninth in line for the Dutch throne, renounced her and her descendants' rights to the throne before officially announcing her engagement on St. Valentine's Day, 1975.
After their wedding, they lived in New York but later moved to the Netherlands, where they built Villa Eikenhorst  in Wassenaar, near The Hague.
She recorded and released several CDs (classical, Broadway) in 2000 and 2002, and was a long-term supporter of the Youth Music Foundation in the Netherlands.
In 1989, she allowed her name to be used for the Prinses Christina Concours, an annual competition held in the Netherlands to encourage the musical talents of children in the Netherlands.
One of her few public performances was at the marriage of her nephew Prince Bernhard Jr.
She also sang at the funerals of both of her parents Princess Juliana and Prince Bernhard in the New Church (Delft).
Early 2019, Christina made headlines when she decided to sell several works of art.
These works came to her through inheritance from the Dutch royal family: art lover William II of the Netherlands.
Death

In June 2018, it was announced that Princess Christina had been diagnosed with bone cancer.
Titles, styles and honours

Honours

National honours

Foreign honours

Ancestry

References

External links

2 also Princess of Lippe-Biesterfeld



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
  AssignClass (a9dc863d-8292-4ad2-b7d7-9b8e9cec2898)
 Call ID: a9dc863d-8292-4ad2-b7d7-9b8e9cec2898
  Args:
    source: :PrincessChristina
    type: :Woman
  AssignClass (9cfe0127-bbd3-45e8-bf5e-537238ddfe06)
 Call ID: 9cfe0127-bbd3-45e8-bf5e-537238ddfe06
  Args:
    source: :PrincessChristina
    type: :Person
  AddLiteral (701fdfe6-595b-4395-87d2-fb76bf72e429)
 Call ID: 701fdfe6-595b-4395-87d2-fb76bf72e429
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1947
    source: :PrincessChristina
  AddLiteral (3b27b78c-b1c4-4405-b89d-1fc0ff7235f0)
 Call ID: 3b27b78c-b1c4-4405-b89d-1fc0ff7235f0
  Args:
    relation: :hasDeathYear
    literal_value: 2019
    literal_type: xsd:integer
    source: :PrincessChristina
  AssignClass (7e2f2942-cf95-4d53-beaa-900e88ecae95)
 Call ID: 7e2f2942-cf95-4d53-beaa-900e88ecae95
  Args:
    source: :QueenJuliana
    type: :Woman
  AssignClass (685a600c-39db-4b0d-96e2-d731c590855b)
 Call ID: 685a600c-39db-4b0d-96e2-d731c590855b
  Args:
    type: :Person
    source: :QueenJuliana
  AssignClass (b78a6def-d02f-4343-aee8-457793dd2748)
 Call ID: b78a6def-d02f-4343-aee8-457793dd2748
  Args:
    source: :PrinceBernhard
    type: :Man
  AssignClass (8b398f95-5337-42e8-a221-daf4b4f7841b)
 Call ID: 8b398f95-5337-42e8-a221-daf4b4f7841b
  Args:
    source: :PrinceBernhard
    type: :Person
  AddTriple (fadc7640-6cc9-49bb-87d1-c8c424cff95b)
 Call ID: fadc7640-6cc9-49bb-87d1-c8c424cff95b
  Args:
    relation: :hasMother
    target: :QueenJuliana
    source: :PrincessChristina
  AddTriple (1302ada7-964c-41c8-abf1-5954371882fa)
 Call ID: 1302ada7-964c-41c8-abf1-5954371882fa
  Args:
    target: :PrinceBernhard
    source: :PrincessChristina
    relation: :hasFather
  AssignClass (9adf50f4-3d64-4ed6-bfed-1e1a46d67302)
 Call ID: 9adf50f4-3d64-4ed6-bfed-1e1a46d67302
  Args:
    type: :Woman
    source: :QueenWilhelmina
  AssignClass (fa6c5fa1-b4d7-4da9-a2a2-cd6d85f0ce33)
 Call ID: fa6c5fa1-b4d7-4da9-a2a2-cd6d85f0ce33
  Args:
    source: :QueenWilhelmina
    type: :Person
  AddTriple (82ea5b35-7e19-413f-9b7a-7cdc73b4c8c2)
 Call ID: 82ea5b35-7e19-413f-9b7a-7cdc73b4c8c2
  Args:
    source: :QueenJuliana
    target: :QueenWilhelmina
    relation: :hasMother
  AssignClass (73dbe742-f34a-4380-90a9-6a1b8e820973)
 Call ID: 73dbe742-f34a-4380-90a9-6a1b8e820973
  Args:
    source: :PrincessBeatrix
    type: :Woman
  AssignClass (68cc620d-7d3f-4631-8bf5-77efd74df047)
 Call ID: 68cc620d-7d3f-4631-8bf5-77efd74df047
  Args:
    source: :PrincessBeatrix
    type: :Person
  AssignClass (55a28adf-e827-4201-93f5-30c71042f541)
 Call ID: 55a28adf-e827-4201-93f5-30c71042f541
  Args:
    source: :PrincessIrene
    type: :Woman
  AssignClass (c5cb37ae-a709-461a-a077-e1cdb8df8ce0)
 Call ID: c5cb37ae-a709-461a-a077-e1cdb8df8ce0
  Args:
    source: :PrincessIrene
    type: :Person
  AssignClass (b4b45874-c0f8-4a33-ab7c-0e0f9a583d33)
 Call ID: b4b45874-c0f8-4a33-ab7c-0e0f9a583d33
  Args:
    source: :PrincessMargriet
    type: :Woman
  AssignClass (958848ab-f03f-4c06-8cf3-79cf0846eb16)
 Call ID: 958848ab-f03f-4c06-8cf3-79cf0846eb16
  Args:
    source: :PrincessMargriet
    type: :Person
  AddTriple (2c893017-bd94-4bd0-9c30-2bf6116e2f02)
 Call ID: 2c893017-bd94-4bd0-9c30-2bf6116e2f02
  Args:
    relation: :isSiblingOf
    source: :PrincessChristina
    target: :PrincessBeatrix
  AddTriple (93a6550b-50ee-4937-add6-0e022d68d9ca)
 Call ID: 93a6550b-50ee-4937-add6-0e022d68d9ca
  Args:
    relation: :isSiblingOf
    source: :PrincessChristina
    target: :PrincessIrene
  AddTriple (7d9db4a4-5d40-4158-b839-aee9e713eb4f)
 Call ID: 7d9db4a4-5d40-4158-b839-aee9e713eb4f
  Args:
    relation: :isSiblingOf
    target: :PrincessMargriet
    source: :PrincessChristina
  AssignClass (d4dccaf6-4b76-494a-a3d4-72eae5126d95)
 Call ID: d4dccaf6-4b76-494a-a3d4-72eae5126d95
  Args:
    source: :PrincessArmgard
    type: :Woman
  AssignClass (2b643583-1c9b-42fd-9399-34ded4077983)
 Call ID: 2b643583-1c9b-42fd-9399-34ded4077983
  Args:
    type: :Person
    source: :PrincessArmgard
  AddTriple (877cd093-dd24-4d0a-8c4c-9313465397d7)
 Call ID: 877cd093-dd24-4d0a-8c4c-9313465397d7
  Args:
    source: :PrinceBernhard
    target: :PrincessArmgard
    relation: :hasMother
  AssignClass (e8a611cf-363a-4a57-9945-dca9141a02fc)
 Call ID: e8a611cf-363a-4a57-9945-dca9141a02fc
  Args:
    type: :Man
    source: :PrinceFelix
  AssignClass (7621c17a-ce3b-41b7-8d3e-4243295b3e62)
 Call ID: 7621c17a-ce3b-41b7-8d3e-4243295b3e62
  Args:
    source: :PrinceFelix
    type: :Person
  AssignClass (8adc392d-7497-4db3-acab-2a596cea68cc)
 Call ID: 8adc392d-7497-4db3-acab-2a596cea68cc
  Args:
    type: :Woman
    source: :PrincessAnne
  AssignClass (a84c9782-eb8e-49fb-a87d-d95a84daec32)
 Call ID: a84c9782-eb8e-49fb-a87d-d95a84daec32
  Args:
    source: :PrincessAnne
    type: :Person
  AssignClass (9272963e-e75c-4b02-a8b3-b0cd5325b0ff)
 Call ID: 9272963e-e75c-4b02-a8b3-b0cd5325b0ff
  Args:
    source: :JorgeGuillermo
    type: :Man
  AssignClass (51abfb2d-e9a9-492b-9323-cb715682a03a)
 Call ID: 51abfb2d-e9a9-492b-9323-cb715682a03a
  Args:
    source: :JorgeGuillermo
    type: :Person
  AssignClass (79f3b08b-e01d-4049-996d-6041ef05e15c)
 Call ID: 79f3b08b-e01d-4049-996d-6041ef05e15c
  Args:
    type: :Man
    source: :PrinceCarlosHugo
  AssignClass (2e48dff5-fb79-4859-9c8e-53c9b27b61a1)
 Call ID: 2e48dff5-fb79-4859-9c8e-53c9b27b61a1
  Args:
    type: :Person
    source: :PrinceCarlosHugo
  AddTriple (f33cd0eb-fe62-4e2b-b425-983c7cc196e1)
 Call ID: f33cd0eb-fe62-4e2b-b425-983c7cc196e1
  Args:
    relation: :isSiblingOf
    source: :PrincessIrene
    target: :PrinceCarlosHugo
  AssignClass (97371d7f-a6f8-4f15-8530-4cdabd105f8d)
 Call ID: 97371d7f-a6f8-4f15-8530-4cdabd105f8d
  Args:
    type: :Man
    source: :PrinceBernhardJr
  AssignClass (4af733e2-0f66-40a4-a796-d77f1dbdaecf)
 Call ID: 4af733e2-0f66-40a4-a796-d77f1dbdaecf
  Args:
    source: :PrinceBernhardJr
    type: :Person
  AssignClass (cf0bf9b0-1b4d-403d-9f87-3f8848694a06)
 Call ID: cf0bf9b0-1b4d-403d-9f87-3f8848694a06
  Args:
    source: :WilliamII
    type: :Man
  AssignClass (eac76a2f-3d51-462a-b87f-ebfcd10965a6)
 Call ID: eac76a2f-3d51-462a-b87f-ebfcd10965a6
  Args:
    source: :WilliamII
    type: :Person
  Finish (a8af0284-93bf-46e1-887a-44f7704b7a22)
 Call ID: a8af0284-93bf-46e1-887a-44f7704b7a22
  Args: