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
Baroness Armgard of Sierstorpff-Cramm, known as Armgard von Cramm (German: Armgard Kunigunde Alharda Agnes Oda von Cramm; 18 December 1883 – 27 April 1971) was the mother of Prince Bernhard of Lippe-Biesterfeld, Prince consort of Queen Juliana of the Netherlands.
Early life

Armgard was born at Bad Driburg, Kingdom of Prussia (now in North Rhine-Westphalia, Germany), as the fourth child and fourth daughter of Baron Aschwin of Sierstorpff-Cramm, and his wife, Baroness Hedwig of Sierstorpff-Driburg.
By birth, she belonged to the ancient German Cramm family.
Marriages

Armgard married on 24 October 1905 at Hanover to Count Bodo von Oeynhausen, an officer in the 8th Hussars in Paderborn, son of Count Erich von Oeynhausen and his wife, Therese von Lenthe.
Armgard married secondly, after the death of her ex-husband, on 4 March 1909 at Oelber, Brunswick to Prince Bernhard of Lippe-Biesterfeld, a younger son of Ernest II, Count of Lippe-Biesterfeld, regent (1897–1904) of the Principality of Lippe, and his wife, Countess Karoline von Wartensleben.
The marriage was at first considered morganatic, as Armgard's family didn't belong to one of the reigning or former reigning families.
Thus, she was created "Countess of Biesterfeld" (German: Gräfin von Biesterfeld) on 8 February 1909.
On 24 February 1916, her marriage was declared equal and she was made "Princess of Lippe-Biesterfeld" (German: Prinzessin zur Lippe-Biesterfeld) along with the style Serene Highness by her brother-in-law, Leopold IV, Prince of Lippe, and this title was extended to her two sons in order to produce a new branch of the Lippe family.
World War II

After the death of her husband in 1934, Armgard moved into Reckenwalde palace with her sons and managed an estate in Wojnowo, Lubusz Voivodeship, Province of Brandenburg (now Wojnowo, Poland), together with her new partner, Alexis Pantchoulidzew, an exiled Russian nobleman.
Alexis accompanied Armgard to the wedding of Bernhard to Princess Juliana.
During World War II Armgard and Alexis were observed by the local Gestapo.
The SS demanded in September 1944 in Recke, one of Armgard's properties, Schloss Woynowo Walde for military purposes.
Armgard and Alexis gave an account of the withdrawal in 1945 of the Wehrmacht behind the Oder-line on their estate at Neumark.
Wim Klinkenberg and some other writers have accused Armgard of sexual promiscuity, intrigue, conspiracy, and – as with her son Aschwin – of Nazi sympathies.
In March 2004, her son Bernhard tried to rectify this image with an open letter to The Times.
Life in the Netherlands

She lived from early 1952 with her partner Alexis Pantchoulidzew in House Warmelo at Diepenheim.
Alexis went on to be the Netherlands' sole representative at the 1956 Summer Olympics, competing in dressage.
Armgard was a convert to Roman Catholicism like her granddaughter Princess Irene, but decided against attending Irene's controversial wedding to Carlos Hugo, Duke of Parma, which neither the Dutch royal family nor any Dutch diplomatic representative attended.
The family nevertheless gathered at Armgard's home for the television coverage of the wedding.
Death

Armgard died on 27 April 1971 in House Warmelo in Diepenheim, at the age of 87.
Zur Lippe-Biesterfeld- Prof. mr. E.J.H.Schrage



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix ns2: <http://www.w3.org/2003/11/swrl#> .
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

ns1:isRuleEnabled a owl:AnnotationProperty .

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

:x a ns2:Variable .

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

:y a ns2:Variable .

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

[] a ns2:Imp ;
    rdfs:label "infer hasSon" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasBrother" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasSister" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (056a2e7f-aa5d-4b83-8798-1044859e2d15)
 Call ID: 056a2e7f-aa5d-4b83-8798-1044859e2d15
  Args:
    type: :Woman
    source: Armgard_von_Cramm
  AssignClass (f59ae842-626f-4848-859c-0f2cca71ebec)
 Call ID: f59ae842-626f-4848-859c-0f2cca71ebec
  Args:
    type: :Person
    source: Armgard_von_Cramm
  AddLiteral (3ed5ea07-4107-4ce5-a9bb-6af41ae86f8b)
 Call ID: 3ed5ea07-4107-4ce5-a9bb-6af41ae86f8b
  Args:
    source: Armgard_von_Cramm
    literal_value: Armgard Kunigunde Alharda Agnes Oda von Cramm
    literal_type: xsd:string
    relation: :knownAs
  AddLiteral (086f4852-7154-41d4-bcd8-b9555f9d814f)
 Call ID: 086f4852-7154-41d4-bcd8-b9555f9d814f
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Armgard_von_Cramm
    literal_value: 1883
  AddLiteral (2c7d2eda-9bad-44d7-b9b2-3cd4c9770cb8)
 Call ID: 2c7d2eda-9bad-44d7-b9b2-3cd4c9770cb8
  Args:
    literal_type: xsd:integer
    source: Armgard_von_Cramm
    literal_value: 1971
    relation: :hasDeathYear
  AssignClass (a830b0fc-6db2-453f-9d92-d2c86df1a6e2)
 Call ID: a830b0fc-6db2-453f-9d92-d2c86df1a6e2
  Args:
    type: :Man
    source: Prince_Bernhard_of_Lippe-Biesterfeld
  AssignClass (d4d550c0-86b5-452c-8608-40f92eaf87e0)
 Call ID: d4d550c0-86b5-452c-8608-40f92eaf87e0
  Args:
    type: :Person
    source: Prince_Bernhard_of_Lippe-Biesterfeld
  AddTriple (a15db47c-393c-4f92-9e15-92ff49c32b5f)
 Call ID: a15db47c-393c-4f92-9e15-92ff49c32b5f
  Args:
    source: Prince_Bernhard_of_Lippe-Biesterfeld
    target: Armgard_von_Cramm
    relation: :hasMother
  AssignClass (783c7671-545c-4d89-b7aa-f42abb69c302)
 Call ID: 783c7671-545c-4d89-b7aa-f42abb69c302
  Args:
    type: :Man
    source: Baron_Aschwin_of_Sierstorpff-Cramm
  AssignClass (51bafd87-4948-4a2b-8868-6a46d3fce575)
 Call ID: 51bafd87-4948-4a2b-8868-6a46d3fce575
  Args:
    type: :Person
    source: Baron_Aschwin_of_Sierstorpff-Cramm
  AssignClass (bce31778-c18a-47ee-84eb-f9fb8cd5171b)
 Call ID: bce31778-c18a-47ee-84eb-f9fb8cd5171b
  Args:
    type: :Woman
    source: Baroness_Hedwig_of_Sierstorpff-Driburg
  AssignClass (fc241aff-47dd-481c-b239-d520b3d66e04)
 Call ID: fc241aff-47dd-481c-b239-d520b3d66e04
  Args:
    type: :Person
    source: Baroness_Hedwig_of_Sierstorpff-Driburg
  AddTriple (d4b238fc-1489-42c7-b6ca-500abd1d9ef6)
 Call ID: d4b238fc-1489-42c7-b6ca-500abd1d9ef6
  Args:
    source: Armgard_von_Cramm
    relation: :hasFather
    target: Baron_Aschwin_of_Sierstorpff-Cramm
  AddTriple (508f6c0d-9978-46df-a9d6-1721269ce2d5)
 Call ID: 508f6c0d-9978-46df-a9d6-1721269ce2d5
  Args:
    source: Armgard_von_Cramm
    target: Baroness_Hedwig_of_Sierstorpff-Driburg
    relation: :hasMother
  AssignClass (2e3ac02a-375a-4321-92a8-5c3cd65d4e84)
 Call ID: 2e3ac02a-375a-4321-92a8-5c3cd65d4e84
  Args:
    type: :Man
    source: Count_Bodo_von_Oeynhausen
  AssignClass (79adb61a-da2b-41b6-bc20-3c384326eeda)
 Call ID: 79adb61a-da2b-41b6-bc20-3c384326eeda
  Args:
    type: :Person
    source: Count_Bodo_von_Oeynhausen
  AddLiteral (2e10790a-fe4b-4770-9832-7e444495272b)
 Call ID: 2e10790a-fe4b-4770-9832-7e444495272b
  Args:
    source: Armgard_von_Cramm
    literal_value: 1905
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AddTriple (2087c6d2-83b1-4f66-a419-48099c74dfa2)
 Call ID: 2087c6d2-83b1-4f66-a419-48099c74dfa2
  Args:
    relation: :hasFather
    target: Count_Erich_von_Oeynhausen
    source: Count_Bodo_von_Oeynhausen
  AddTriple (d63f0330-73e3-4058-a769-e511646f8b6e)
 Call ID: d63f0330-73e3-4058-a769-e511646f8b6e
  Args:
    relation: :hasMother
    target: Therese_von_Lenthe
    source: Count_Bodo_von_Oeynhausen
  AssignClass (6db1ee46-40e1-4984-9921-4ab1e68857a7)
 Call ID: 6db1ee46-40e1-4984-9921-4ab1e68857a7
  Args:
    type: :Man
    source: Count_Erich_von_Oeynhausen
  AssignClass (8424177d-3c05-4edf-ac85-06fa0c3d6bcb)
 Call ID: 8424177d-3c05-4edf-ac85-06fa0c3d6bcb
  Args:
    type: :Person
    source: Count_Erich_von_Oeynhausen
  AssignClass (811cd7cc-9632-4d95-b55f-ec360e4b3cec)
 Call ID: 811cd7cc-9632-4d95-b55f-ec360e4b3cec
  Args:
    type: :Woman
    source: Therese_von_Lenthe
  AssignClass (0dc34b7b-04f8-436f-898d-ce6ba6c577d6)
 Call ID: 0dc34b7b-04f8-436f-898d-ce6ba6c577d6
  Args:
    type: :Person
    source: Therese_von_Lenthe
  AssignClass (82810568-cbcd-4dcc-b95f-0790ad2795ad)
 Call ID: 82810568-cbcd-4dcc-b95f-0790ad2795ad
  Args:
    type: :Man
    source: Prince_Bernhard_of_Lippe-Biesterfeld_Senior
  AssignClass (1c65cde8-34d7-4b9f-884c-bb0965d2c548)
 Call ID: 1c65cde8-34d7-4b9f-884c-bb0965d2c548
  Args:
    type: :Person
    source: Prince_Bernhard_of_Lippe-Biesterfeld_Senior
  AddLiteral (b5bc0767-770b-4e01-9785-cd9c16ad052c)
 Call ID: b5bc0767-770b-4e01-9785-cd9c16ad052c
  Args:
    literal_type: xsd:integer
    literal_value: 1909
    source: Armgard_von_Cramm
    relation: :hasMarriageYear
  AddTriple (1fb68b90-7b31-4b86-8929-155b08e5fd42)
 Call ID: 1fb68b90-7b31-4b86-8929-155b08e5fd42
  Args:
    relation: :hasFather
    target: Ernest_II_Count_of_Lippe-Biesterfeld
    source: Prince_Bernhard_of_Lippe-Biesterfeld_Senior
  AddTriple (0441c05d-69bd-4d5e-b17e-9b957e21fb16)
 Call ID: 0441c05d-69bd-4d5e-b17e-9b957e21fb16
  Args:
    source: Prince_Bernhard_of_Lippe-Biesterfeld_Senior
    target: Countess_Karoline_von_Wartensleben
    relation: :hasMother
  AssignClass (38cfcebb-3860-4737-8011-a724076081da)
 Call ID: 38cfcebb-3860-4737-8011-a724076081da
  Args:
    type: :Man
    source: Ernest_II_Count_of_Lippe-Biesterfeld
  AssignClass (5d0985d4-bb2d-4582-b975-c0bd4acc660f)
 Call ID: 5d0985d4-bb2d-4582-b975-c0bd4acc660f
  Args:
    type: :Person
    source: Ernest_II_Count_of_Lippe-Biesterfeld
  AssignClass (b4febd0b-986c-4bda-ab08-1f19e9fd052a)
 Call ID: b4febd0b-986c-4bda-ab08-1f19e9fd052a
  Args:
    type: :Woman
    source: Countess_Karoline_von_Wartensleben
  AssignClass (d327673b-6b20-4e7a-a154-59de8e662854)
 Call ID: d327673b-6b20-4e7a-a154-59de8e662854
  Args:
    type: :Person
    source: Countess_Karoline_von_Wartensleben
  Finish (295690a3-111d-4403-89c7-aceb89b4bb18)
 Call ID: 295690a3-111d-4403-89c7-aceb89b4bb18
  Args: