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
Prince Bernhard of Lippe (Bernhard Kasimir Wilhelm Friedrich Gustav Heinrich Eduard; 26 August 1872 – 19 June 1934) was a member of the Lippe-Biesterfeld line of the House of Lippe.
He was the father of Prince Bernhard of Lippe-Biesterfeld, the prince consort of Queen Juliana of the Netherlands.
Biography

Prince Bernhard of Lippe, born as Count of Lippe-Biesterfeld in Oberkassel on 26 August 1872, was the 2nd son of Ernest II, Count of Lippe-Biesterfeld, regent (1897–1904) of Principality of Lippe, and his wife Countess Karoline von Wartensleben.
He was a younger brother of Leopold IV, Prince of Lippe, who succeeded as reigning Prince of Lippe in 1905.
The Lippe-Biesterfeld family had lived at Oberkassel, Bonn, ever since 1770, when count Frederick William (1737–1803) had married Elisabeth Johanna, Edle von Meinertzhagen (1752–1811), who inherited a small manor house at Oberkassel where the couple moved from Biesterfeld in 1770, and which became the home to the family for the following 209 years.
The manor house and farm at Biesterfeld were demolished around 1820.
Prince Bernhard acquired the Reckenwalde castle in eastern Brandenburg (today Wojnowo, Poland), the family's new estate, where his children grew up.
On 4 March 1909, Bernhard entered into a morganatic marriage with Baroness Armgard von Sierstorpff-Cramm, widowed Countess von Oeynhausen.
Before this marriage, his wife was granted the title Countess of Biesterfeld (Gräfin von Biesterfeld) on 8 February 1909.
She and her two sons Bernhard and Aschwin were created Princess (Prince) of Lippe-Biesterfeld (Prinzessin (Prinz) zur Lippe-Biesterfeld) on 24 February 1916 with the style Serene Highness, which brought their children into a more senior place in the line of succession, in which they hitherto had been the very last.
The suffix Biesterfeld was revived to mark the beginning of a new cadet line.
Bernhard died in Munich, aged 61.



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
  AssignClass (2d3e1cfe-e161-4af0-8e21-773a83749210)
 Call ID: 2d3e1cfe-e161-4af0-8e21-773a83749210
  Args:
    type: :Man
    source: :PrinceBernhardOfLippe
  AssignClass (3588956b-4894-4541-8bc5-7239a11a712d)
 Call ID: 3588956b-4894-4541-8bc5-7239a11a712d
  Args:
    type: :Person
    source: :PrinceBernhardOfLippe
  AddLiteral (1c7e5f53-3ea4-4b60-b718-45ac3e375be4)
 Call ID: 1c7e5f53-3ea4-4b60-b718-45ac3e375be4
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1872
    source: :PrinceBernhardOfLippe
  AddLiteral (5f9f6f2f-a67e-48fe-a15b-d9fa8fa19701)
 Call ID: 5f9f6f2f-a67e-48fe-a15b-d9fa8fa19701
  Args:
    source: :PrinceBernhardOfLippe
    literal_value: 1934
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (9eb13fb0-f4a9-44c7-a3cf-7a513f948583)
 Call ID: 9eb13fb0-f4a9-44c7-a3cf-7a513f948583
  Args:
    type: :Man
    source: :PrinceBernhardOfLippeBiesterfeld
  AssignClass (92534c81-a1f9-4db3-9e9f-b2f9066416db)
 Call ID: 92534c81-a1f9-4db3-9e9f-b2f9066416db
  Args:
    type: :Person
    source: :PrinceBernhardOfLippeBiesterfeld
  AddTriple (b7c19294-cae0-43c6-901e-cc43b9dfa447)
 Call ID: b7c19294-cae0-43c6-901e-cc43b9dfa447
  Args:
    source: :PrinceBernhardOfLippeBiesterfeld
    target: :PrinceBernhardOfLippe
    relation: :isSonOf
  AssignClass (5f5d2533-589e-4bdc-8029-6994b5537102)
 Call ID: 5f5d2533-589e-4bdc-8029-6994b5537102
  Args:
    type: :Man
    source: :ErnestII_CountOfLippeBiesterfeld
  AssignClass (d5e7481d-e409-4290-b2f1-282e0a51eb3f)
 Call ID: d5e7481d-e409-4290-b2f1-282e0a51eb3f
  Args:
    type: :Person
    source: :ErnestII_CountOfLippeBiesterfeld
  AddTriple (d932cb65-a419-41be-9cbc-9ab4e1d28df9)
 Call ID: d932cb65-a419-41be-9cbc-9ab4e1d28df9
  Args:
    relation: :isSonOf
    source: :PrinceBernhardOfLippe
    target: :ErnestII_CountOfLippeBiesterfeld
  AssignClass (e33c4929-9cbc-4c03-a6a4-eb0af6bb5789)
 Call ID: e33c4929-9cbc-4c03-a6a4-eb0af6bb5789
  Args:
    type: :Woman
    source: :CountessKarolineVonWartensleben
  AssignClass (3e30c8a9-e92e-4b9b-8f77-d0e029fc9b89)
 Call ID: 3e30c8a9-e92e-4b9b-8f77-d0e029fc9b89
  Args:
    type: :Person
    source: :CountessKarolineVonWartensleben
  AddTriple (658a4c27-19af-49cb-ba2a-0de5049d48ff)
 Call ID: 658a4c27-19af-49cb-ba2a-0de5049d48ff
  Args:
    relation: :isMotherOf
    target: :PrinceBernhardOfLippe
    source: :CountessKarolineVonWartensleben
  AssignClass (0aab0809-4037-493a-ba92-615ca7f23bfa)
 Call ID: 0aab0809-4037-493a-ba92-615ca7f23bfa
  Args:
    type: :Man
    source: :LeopoldIV_PrinceOfLippe
  AssignClass (9a91dc48-6a2e-4d6d-bf1f-91150a6028b1)
 Call ID: 9a91dc48-6a2e-4d6d-bf1f-91150a6028b1
  Args:
    type: :Person
    source: :LeopoldIV_PrinceOfLippe
  AddTriple (e02f5321-9bb2-486e-8d3b-1fcbf3a7cb34)
 Call ID: e02f5321-9bb2-486e-8d3b-1fcbf3a7cb34
  Args:
    relation: :isBrotherOf
    source: :PrinceBernhardOfLippe
    target: :LeopoldIV_PrinceOfLippe
  AssignClass (e3030671-04bc-4b0b-8c03-6c2350f266ff)
 Call ID: e3030671-04bc-4b0b-8c03-6c2350f266ff
  Args:
    type: :Man
    source: :CountFrederickWilliam
  AssignClass (ef05d4ab-8616-49f2-8479-bba53b2ecad0)
 Call ID: ef05d4ab-8616-49f2-8479-bba53b2ecad0
  Args:
    type: :Person
    source: :CountFrederickWilliam
  AddLiteral (87b9e61c-0cdc-49b3-8b65-fa8438e6e0f5)
 Call ID: 87b9e61c-0cdc-49b3-8b65-fa8438e6e0f5
  Args:
    literal_value: 1737
    source: :CountFrederickWilliam
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (9975dc54-86c7-4d5e-98f6-061109d1d697)
 Call ID: 9975dc54-86c7-4d5e-98f6-061109d1d697
  Args:
    literal_value: 1803
    source: :CountFrederickWilliam
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (909081ea-7755-475c-8828-ef23ba2cf73d)
 Call ID: 909081ea-7755-475c-8828-ef23ba2cf73d
  Args:
    type: :Woman
    source: :ElisabethJohanna_EdleVonMeinertzhagen
  AssignClass (0a8e8da2-e1a6-4203-879e-c1157e26221d)
 Call ID: 0a8e8da2-e1a6-4203-879e-c1157e26221d
  Args:
    type: :Person
    source: :ElisabethJohanna_EdleVonMeinertzhagen
  AddLiteral (f38a27a8-2dc1-4a62-8ef8-9f84bfb61acb)
 Call ID: f38a27a8-2dc1-4a62-8ef8-9f84bfb61acb
  Args:
    literal_value: 1752
    source: :ElisabethJohanna_EdleVonMeinertzhagen
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (823dcf51-ccb2-4350-9c8e-fe8270d81956)
 Call ID: 823dcf51-ccb2-4350-9c8e-fe8270d81956
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1811
    source: :ElisabethJohanna_EdleVonMeinertzhagen
  AddLiteral (7a59891a-c71d-4b87-a415-89380332cd6a)
 Call ID: 7a59891a-c71d-4b87-a415-89380332cd6a
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: :CountFrederickWilliam
    literal_value: 1770
  AssignClass (b8c818ad-a340-4d89-abe5-1140ac94e031)
 Call ID: b8c818ad-a340-4d89-abe5-1140ac94e031
  Args:
    type: :Woman
    source: :BaronessArmgardVonSierstorpffCramm
  AssignClass (4f3a646c-e3b5-48b5-8c71-1ab6d69fb845)
 Call ID: 4f3a646c-e3b5-48b5-8c71-1ab6d69fb845
  Args:
    type: :Person
    source: :BaronessArmgardVonSierstorpffCramm
  AddLiteral (e4881e36-142a-48ed-ae1a-c4c803168c74)
 Call ID: e4881e36-142a-48ed-ae1a-c4c803168c74
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1909
    source: :PrinceBernhardOfLippe
  AssignClass (81682966-d369-4019-a27a-ed1ecef10676)
 Call ID: 81682966-d369-4019-a27a-ed1ecef10676
  Args:
    type: :Man
    source: :Aschwin
  AssignClass (131389ef-b172-4ae0-9bec-22eedf86c8f4)
 Call ID: 131389ef-b172-4ae0-9bec-22eedf86c8f4
  Args:
    type: :Person
    source: :Aschwin
  AddTriple (ca06495d-9190-47b5-82a3-c7803942fdd5)
 Call ID: ca06495d-9190-47b5-82a3-c7803942fdd5
  Args:
    relation: :isSonOf
    target: :PrinceBernhardOfLippe
    source: :Aschwin
  Finish (a682ee0c-ec48-4fb9-9dba-5e7375d4ea75)
 Call ID: a682ee0c-ec48-4fb9-9dba-5e7375d4ea75
  Args: