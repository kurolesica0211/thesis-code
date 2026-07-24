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
Princess Isabelle of Orléans (Isabelle Marie Laure Mercédès Ferdinande; 7 May 1878 – 21 April 1961) was a member of the French Orleanist royal family and by marriage Duchess of Guise.
Biography

Early life

Isabelle was born at the Château d'Eu in Eu, France, the third daughter and fifth (fourth surviving) child of Prince Philippe, Count of Paris and Infanta Maria Isabel of Spain.
Marriage and issue

As a young woman, Isabelle had many suitors, chief among them being the future Albert I of Belgium.
Albert, however, was forced to end the courtship under pressure from his uncle King Leopold II, who feared that a marriage to the daughter of an exiled pretender to the French throne would result in backlash from the republican government in Paris.
On 30 October 1899, Isabelle married her first cousin Prince Jean, Duke of Guise.
Jean was the son of prince Robert, Duke of Chartres and Françoise d'Orléans.
Upon the death of her brother, Philippe of Orléans, Duke of Orléans, claimant to the throne of France as "Philip VIII", the Duke of Guise became, at least for his Orleanist supporters, titular king of France as "Jean III".
The couple had four children:


Princess Isabelle died in Larache, Morocco, on 21 April 1962 at age 82.



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
  AssignClass (6c53279c-6703-4f6e-a75b-36776c0be51f)
 Call ID: 6c53279c-6703-4f6e-a75b-36776c0be51f
  Args:
    type: :Woman
    source: :Isabelle_of_Orleans
  AssignClass (36985d07-4806-428f-b93e-2892d35600fb)
 Call ID: 36985d07-4806-428f-b93e-2892d35600fb
  Args:
    type: :Person
    source: :Isabelle_of_Orleans
  AddLiteral (3daf5851-c09a-4989-8346-bf9c4d225269)
 Call ID: 3daf5851-c09a-4989-8346-bf9c4d225269
  Args:
    relation: :hasBirthYear
    source: :Isabelle_of_Orleans
    literal_type: xsd:integer
    literal_value: 1878
  AddLiteral (4a0ae2eb-b801-4d89-af87-5113512726dc)
 Call ID: 4a0ae2eb-b801-4d89-af87-5113512726dc
  Args:
    literal_value: 1962
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: :Isabelle_of_Orleans
  AssignClass (b511b620-5b02-43d6-a075-f1fd7e7a7954)
 Call ID: b511b620-5b02-43d6-a075-f1fd7e7a7954
  Args:
    type: :Man
    source: :Prince_Philippe_Count_of_Paris
  AssignClass (ad6eb9aa-afa4-40d4-9c00-d948a61070fa)
 Call ID: ad6eb9aa-afa4-40d4-9c00-d948a61070fa
  Args:
    type: :Person
    source: :Prince_Philippe_Count_of_Paris
  AssignClass (be60af41-cafc-447a-b9b4-bef981238446)
 Call ID: be60af41-cafc-447a-b9b4-bef981238446
  Args:
    type: :Woman
    source: :Infanta_Maria_Isabel_of_Spain
  AssignClass (6aac85aa-e3a9-4384-a560-bda042d2609f)
 Call ID: 6aac85aa-e3a9-4384-a560-bda042d2609f
  Args:
    type: :Person
    source: :Infanta_Maria_Isabel_of_Spain
  AddTriple (ef7e609e-2d75-4076-b888-0706fe04901f)
 Call ID: ef7e609e-2d75-4076-b888-0706fe04901f
  Args:
    target: :Prince_Philippe_Count_of_Paris
    source: :Isabelle_of_Orleans
    relation: :hasFather
  AddTriple (d9952dd8-2d65-4252-a34d-a8635b5f2a9a)
 Call ID: d9952dd8-2d65-4252-a34d-a8635b5f2a9a
  Args:
    source: :Isabelle_of_Orleans
    relation: :hasMother
    target: :Infanta_Maria_Isabel_of_Spain
  AssignClass (822ce27e-b1bf-4e6c-8b9f-7436441656bc)
 Call ID: 822ce27e-b1bf-4e6c-8b9f-7436441656bc
  Args:
    type: :Man
    source: :Prince_Jean_Duke_of_Guise
  AssignClass (f0623ae7-f90f-411e-a8b5-cf9ce1e3204c)
 Call ID: f0623ae7-f90f-411e-a8b5-cf9ce1e3204c
  Args:
    type: :Person
    source: :Prince_Jean_Duke_of_Guise
  AddLiteral (61e384d5-25b2-47b3-a6b1-746d3a8321ae)
 Call ID: 61e384d5-25b2-47b3-a6b1-746d3a8321ae
  Args:
    source: :Isabelle_of_Orleans
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 1899
  AddTriple (db56b635-fb0b-41ce-9ade-34adcc8412b6)
 Call ID: db56b635-fb0b-41ce-9ade-34adcc8412b6
  Args:
    source: :Isabelle_of_Orleans
    relation: :hasRelation
    target: :Prince_Jean_Duke_of_Guise
  AssignClass (c8626c67-9bb1-4175-a253-1912624a8d63)
 Call ID: c8626c67-9bb1-4175-a253-1912624a8d63
  Args:
    type: :Man
    source: :Prince_Robert_Duke_of_Chartres
  AssignClass (ae04359b-5f6f-4d27-97f5-9d7ce4492a85)
 Call ID: ae04359b-5f6f-4d27-97f5-9d7ce4492a85
  Args:
    type: :Person
    source: :Prince_Robert_Duke_of_Chartres
  AssignClass (5980a043-12a2-4ef0-9d78-680c9d211d4f)
 Call ID: 5980a043-12a2-4ef0-9d78-680c9d211d4f
  Args:
    type: :Woman
    source: :Francoise_d_Orleans
  AssignClass (20a96bad-b399-482b-ad9d-435b7629ab34)
 Call ID: 20a96bad-b399-482b-ad9d-435b7629ab34
  Args:
    type: :Person
    source: :Francoise_d_Orleans
  AddTriple (adf01d6c-31ab-463d-ad47-75a3602be7b7)
 Call ID: adf01d6c-31ab-463d-ad47-75a3602be7b7
  Args:
    target: :Prince_Robert_Duke_of_Chartres
    relation: :hasFather
    source: :Prince_Jean_Duke_of_Guise
  AddTriple (c6511164-99c5-4f97-8773-05d140f3cc24)
 Call ID: c6511164-99c5-4f97-8773-05d140f3cc24
  Args:
    source: :Prince_Jean_Duke_of_Guise
    relation: :hasMother
    target: :Francoise_d_Orleans
  AssignClass (c0f031eb-2ba1-49c1-84c3-d9adfa6dc8e0)
 Call ID: c0f031eb-2ba1-49c1-84c3-d9adfa6dc8e0
  Args:
    type: :Man
    source: :Philippe_of_Orleans_Duke_of_Orleans
  AssignClass (aabaf8a7-1f84-4931-8435-08ecbecce663)
 Call ID: aabaf8a7-1f84-4931-8435-08ecbecce663
  Args:
    type: :Person
    source: :Philippe_of_Orleans_Duke_of_Orleans
  AddTriple (081a2a16-d2be-4229-8a1e-fda3991c0024)
 Call ID: 081a2a16-d2be-4229-8a1e-fda3991c0024
  Args:
    relation: :hasBrother
    source: :Isabelle_of_Orleans
    target: :Philippe_of_Orleans_Duke_of_Orleans
  Finish (a16c4942-f8e5-4b05-a79d-f8f9ebaaf2ff)
 Call ID: a16c4942-f8e5-4b05-a79d-f8f9ebaaf2ff
  Args: